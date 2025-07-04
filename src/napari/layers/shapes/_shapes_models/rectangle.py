import numpy as np

from napari.layers.shapes._shapes_models.shape import Shape
from napari.layers.shapes._shapes_utils import find_corners, rectangle_to_box
from napari.utils.translations import trans


class Rectangle(Shape):
    """Class for a single rectangle

    Parameters
    ----------
    data : (4, D) or (2, 2) array
        Either a (2, 2) array specifying the two corners of an axis aligned
        rectangle, or a (4, D) array specifying the four corners of a bounding
        box that contains the rectangle. These need not be axis aligned.
    edge_width : float
        thickness of lines and edges.
    z_index : int
        Specifier of z order priority. Shapes with higher z order are displayed
        ontop of others.
    dims_order : (D,) list
        Order that the dimensions are to be rendered in.
    """

    def __init__(
        self,
        data,
        *,
        edge_width=1,
        z_index=0,
        dims_order=None,
        ndisplay=2,
    ) -> None:
        super().__init__(
            edge_width=edge_width,
            z_index=z_index,
            dims_order=dims_order,
            ndisplay=ndisplay,
        )

        self._closed = True
        self.data = data
        self.name = 'rectangle'

    @property
    def data(self):
        """(4, D) array: rectangle vertices."""
        return self._data

    @data.setter
    def data(self, data):
        data = np.array(data).astype(np.float32)

        if len(self.dims_order) != data.shape[1]:
            self._dims_order = list(range(data.shape[1]))

        if len(data) == 2 and data.shape[1] == 2:
            data = find_corners(data)

        if len(data) != 4:
            raise ValueError(
                trans._(
                    'Data shape does not match a rectangle. Rectangle expects four corner vertices, {number} provided.',
                    deferred=True,
                    number=len(data),
                )
            )

        self._data = data
        self._bounding_box = np.array(
            [
                np.min(data, axis=0),
                np.max(data, axis=0),
            ]
        )
        self._update_displayed_data()

    def _update_displayed_data(self) -> None:
        """Update the data that is to be displayed."""
        # Add four boundary lines and then two triangles for each
        self._clean_cache()
        data_displayed = self.data_displayed
        self._set_meshes(data_displayed, face=False)
        self._face_vertices = data_displayed
        self._face_triangles = np.array([[0, 1, 2], [0, 2, 3]])
        # The data displayed are in this case the four corners
        self._box = rectangle_to_box(data_displayed)  # type: ignore[arg-type]
        self.slice_key = self._bounding_box[:, self.dims_not_displayed].astype(
            'int'
        )
