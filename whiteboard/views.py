from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Whiteboard, Drawing

# Create your views here.


class WhiteBoardMultiView(APIView):
    permission_classes = [IsAuthenticated]

    class WhiteBoardPostSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)

    class WhiteBoardModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Whiteboard
            fields = ("id", "name")

    def get(self, *args, **kwargs):
        user_obj = self.request.user
        white_board_objs = Whiteboard.objects.filter(user=user_obj)

        return Response(
            self.WhiteBoardModelSerializer(white_board_objs, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, *args, **kwargs):
        white_board_post_serializer = self.WhiteBoardPostSerializer(
            data=self.request.data
        )

        if not white_board_post_serializer.is_valid():
            return Response(
                white_board_post_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        white_board_obj = Whiteboard.objects.create(
            name=white_board_post_serializer.validated_data.get("name"),
            user=self.request.user,
        )

        return Response(
            self.WhiteBoardModelSerializer(white_board_obj).data,
            status=status.HTTP_201_CREATED,
        )


class WhiteBoardView(APIView):
    permission_classes = [IsAuthenticated]

    class KwargsValidationSerializer(serializers.Serializer):
        white_board_id = serializers.IntegerField(required=True)

    class WhiteBoardPatchSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)

    class WhiteBoardModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Whiteboard
            fields = [
                "id",
                "name",
                "created_at",
            ]

    def get(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)
        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        white_board_id = kwargs_serializer.validated_data.get("white_board_id")

        try:
            white_board_obj = Whiteboard.objects.get(id=white_board_id)
        except Whiteboard.DoesNotExist:
            msg = {"white_board_id": "Id Does Not Exist"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            self.WhiteBoardModelSerializer(white_board_obj).data,
            status=status.HTTP_200_OK,
        )

    def patch(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)
        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        white_board_id = kwargs_serializer.validated_data.get("workspace_id")

        try:
            # request.user only can do patch
            white_board_obj = Whiteboard.objects.get(
                id=white_board_id, user=self.request.user
            )
        except Whiteboard.DoesNotExist:
            msg = {"white_board_id": "Id Does Not Exist"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        patch_serializer = self.WhiteBoardPatchSerializer(data=self.request.data)
        if not patch_serializer.is_valid():
            return Response(patch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = patch_serializer.validated_data.get("name", None)

        white_board_obj.name = name

        white_board_obj.save()

        return Response(
            self.WhiteBoardModelSerializer(white_board_obj).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)
        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        white_board_id = kwargs_serializer.validated_data.get("workspace_id")

        try:
            # request.user only can do delete
            white_board_obj = Whiteboard.objects.get(
                id=white_board_id, user=self.request.user
            )
        except Whiteboard.DoesNotExist:
            msg = {"white_board_id": "Id Does Not Exist"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        white_board_obj.delete()

        return Response(
            status=status.HTTP_200_OK,
        )


class DrawingMultiView(APIView):
    permission_classes = [IsAuthenticated]

    class KwargsValidationSerializer(serializers.Serializer):
        white_board_id = serializers.IntegerField(required=True)

    class DrawingPostSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)

    class DrawingModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = Drawing
            fields = ("id", "name")

    def get(self, *args, **kwargs):

        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)
        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        white_board_id = kwargs_serializer.validated_data.get("workspace_id")
        user_obj = self.request.user
        drawing_objs = Drawing.objects.filter(white_board=white_board_id)
        
        return Response(
            self.DrawingModelSerializer(drawing_objs, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)
        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        white_board_id = kwargs_serializer.validated_data.get("workspace_id")

        try:
            white_board_obj = Whiteboard.objects.get(id=white_board_id)
        except Whiteboard.DoesNotExist:
            msg = {"white_board_id": "Id Does Not Exist"}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        white_board_post_serializer = self.DrawingPostSerializer(
            data=self.request.data
        )
        if not white_board_post_serializer.is_valid():
            return Response(
                white_board_post_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        drawing_obj = Drawing.objects.create(
            name=white_board_post_serializer.validated_data.get("name"),
            white_board=white_board_obj,
        )
        
        return Response(
            self.DrawingModelSerializer(drawing_obj).data,
            status=status.HTTP_201_CREATED,
        )