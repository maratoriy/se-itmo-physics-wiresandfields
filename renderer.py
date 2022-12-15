import matplotlib as mpl
import os
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Circle
from system import *
from wire import *
from draggablepoint import *
from matplotlib.backend_tools import ToolBase, ToolToggleBase, cursors

plt.rcParams['toolbar'] = 'toolmanager'

class RendererToolBase(ToolBase):
    def __init__(self, toolmanager, name, *args, **kwargs):
        self.renderer = kwargs.pop('renderer')
        super().__init__(toolmanager, name)

class ChangeDensity(RendererToolBase):
    description = "Change density of the plot"

    def __init__(self, toolmanager, name, *args, **kwargs):
        super().__init__(toolmanager, name, *args, **kwargs)
        self.mult = kwargs.pop('mult')
        if(self.mult > 1):
            self.image = os.path.abspath("up.png")
        else:
            self.image =  os.path.abspath("down.png")

    def trigger(self, sender, event, data=None):
        self.renderer.density*=self.mult
        self.renderer.update()
        self.canvas.draw()

class CursorTool(RendererToolBase, ToolToggleBase):
    cursor = cursors.SELECT_REGION

    def enable(self, event=None):
        self._idPress = self.figure.canvas.mpl_connect(
            'button_press_event', self._press)
        self._idScroll = self.figure.canvas.mpl_connect(
            'scroll_event', self._scroll)

    def disable(self, event=None):
        self.figure.canvas.mpl_disconnect(self._idPress)
        self.figure.canvas.mpl_disconnect(self._idScroll)

    def _press(self, event):
        x, y = event.xdata, event.ydata

        if (x is not None and y is not None and event.inaxes is not None):
            if(event.button == MouseButton.LEFT):
               self._left(event)
            if(event.button == MouseButton.RIGHT):
               self._right(event)

        self.renderer.update()
        self.canvas.draw()

    def _left(self, event):
        pass

    def _right(self, event):
        pass

    def _scroll(self, event):
        pass


class AddNewWire(CursorTool):
    elec = 10
    description = "Add a new wire\nPoint to location\nLeft or right click determines direction\nUse scroll to change electric conductivity "
    image = os.path.abspath("add.png")

    def enable(self, event=None):
        super(AddNewWire, self).enable(event)
        self.toolmanager.message_event("Conductivity of wire: "+str(self.elec))

    def _scroll(self, event):
        if(event.button=="up"):
            self.elec+=1
        if(event.button=="down" and self.elec>1):
            self.elec-=1
        self.toolmanager.message_event("Conductivity of wire: "+str(self.elec))

    def _left(self, event):
        self.renderer.system.addPoint(Wire(event.xdata, event.ydata, 0.5, self.elec))

    def _right(self, event):
        self.renderer.system.addPoint(Wire(event.xdata, event.ydata, 0.5, -self.elec))


class RemoveWire(CursorTool):
    description = "Remove wire\nPoint to wire and use left click"
    image = os.path.abspath("remove.png")
    def _left(self, event):
        for point in self.renderer.system.points:
            if(point.hit(event.xdata, event.ydata)):
                self.renderer.system.removePoint(point)





class Renderer():
    def __init__(self, system, XMAX, YMAX, density, rx, ry):
        self.system = system
        self.XMAX, self.YMAX = XMAX, YMAX
        self.density = density
        self.rx, self.ry = rx, ry

    def launch(self):
        self.figure, self.ax = plt.subplots()
        self.update()
        self.ax.set_xlabel('$x$')
        self.ax.set_ylabel('$y$')
        self.ax.set_xlim(-self.XMAX, self.XMAX)
        self.ax.set_ylim(-self.YMAX, self.YMAX)
        self.ax.set_aspect('equal')
        self.figure.canvas.manager.toolmanager.add_tool('DensityUp', ChangeDensity, renderer=self, mult=1.2)
        self.figure.canvas.manager.toolmanager.add_tool('DensityDown', ChangeDensity, renderer=self, mult=1/1.2)
        self.figure.canvas.manager.toolmanager.add_tool('AddWire', AddNewWire, renderer=self)
        self.figure.canvas.manager.toolmanager.add_tool('RemoveWire', RemoveWire, renderer=self)
        self.figure.canvas.manager.toolbar.add_tool('DensityUp', 'system')
        self.figure.canvas.manager.toolbar.add_tool('DensityDown', 'system')
        self.figure.canvas.manager.toolbar.add_tool('AddWire', 'system')
        self.figure.canvas.manager.toolbar.add_tool('RemoveWire', 'system')
        to_remove = ['forward', 'back', 'help']
        for i in to_remove:
            self.figure.canvas.manager.toolmanager.remove_tool(i)
        plt.show()

    def update(self):
        self.clear()
        self.dfield()
        self.dpoints()
        self.dwalls()

    def clear(self):
        plt.cla()

    def dfield(self):
        x = np.linspace(-self.XMAX, self.XMAX, self.rx)
        y = np.linspace(-self.YMAX, self.YMAX, self.ry)
        X, Y = np.meshgrid(x, y)
        [Vx, Vy] = self.system.field(X, Y)

        if len(Vx) and len(Vy) and len(self.system.points)>0:
            self.ax.streamplot(x, y, -Vy, Vx, color=(2 * np.log(np.hypot(Vx, Vy))), linewidth=1, cmap=plt.cm.inferno,
                               density=self.density, arrowstyle='->', arrowsize=1.5)

    def dpoints(self):
        self.draggables = []
        for point in self.system.points:
            circle = Circle((point.x, point.y), point.size,
                            color=plt.cm.RdBu(mpl.colors.Normalize(vmin=-10, vmax=10)(-point.electric)), zorder=100)
            self.ax.add_patch(circle)
            draggable = DraggablePoint(circle, self.update, point)
            draggable.connect()
            self.draggables.append(draggable)

    def dwalls(self):
        for wall in self.system.walls:
            self.ax.plot([wall.x1, wall.y1], [wall.x2, wall.y2], marker='o')