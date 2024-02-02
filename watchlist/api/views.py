from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


from watchlist.models import Movie
from watchlist.api.serializers import MovieSerializer

# Create your views here.
# --------------------------------------------------------------------------
# ------------------ using APIView class based view decorator --------------
# --------------------------------------------------------------------------

class MovieListAPIView(APIView):

    def get(self, request):
        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)
        return Response({'data': serializer.data, 'msg':'Success. request processed.'}, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'msg': 'Success. record created.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': f'Error. Unable to create record with data {serializer.data}'},
                            status=status.HTTP_400_BAD_REQUEST)



# --------------------------------------------------------------------------
# ------------------------- using api_view decorator -----------------------
# --------------------------------------------------------------------------

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)

#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_movie_details(request, pk):
    if request.method == 'GET':
        if pk:
            try:
                movie = Movie.objects.get(pk=pk)
                serializer = MovieSerializer(movie)

                return Response({'data': serializer.data, 'msg': 'request successfully processed.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error':f"No records found with id {pk} to fetch the movie details."}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({'error': f'No record found with id {pk} to fetch the details.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if pk:
            try:
                movie = Movie.objects.get(pk=pk)
                serializer = MovieSerializer(instance=movie, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response({'data': serializer.data, 'msg': 'request successfully processed.'}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors)
            except Exception as e:
                return Response({'error': f'Error while updating record with id {pk} {e}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f'No record found with id {pk} to update the record.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        if pk:
            try:
                movie = Movie.objects.get(pk=pk)
                serializer = MovieSerializer(instance=movie, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors)
            except Exception as e:
                return Response({'error': f'Error while updating record with id {pk} {e}'})
        else:
            return Response({'error': f'No record found with id {pk} to update the record.'})
        
    if request.method == 'DELETE':
        if pk:
            try:
                movie = Movie.objects.get(pk=pk)
                movie.delete()
            
            except Exception as e:
                return Response({'error': f'Error while deleting record with id {pk}. {e}'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': f'No record found with id {pk} to update the record.'}, 
                            status=status.HTTP_404_NOT_FOUND)
