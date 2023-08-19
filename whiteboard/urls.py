from django.urls import path
from .views import WhiteBoardMultiView, WhiteBoardView, DrawingMultiView

urlpatterns = [
    path(
        "whiteboard/",
        WhiteBoardMultiView.as_view(),
        name="White_board_multi_view",
    ),
    path(
        "whiteboard/<white_board_id>/",
        WhiteBoardView.as_view(),
        name="White_board_view",
    ),
    path(
        "whiteboard/<white_board_id>/drawing/",
        DrawingMultiView.as_view(),
        name="drawing_multi_view",
    ), # get / post drawings inside white_board
]
