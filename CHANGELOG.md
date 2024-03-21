# Changelog


## 2024-03-21
### Updated

### Todo
- prepa ppt et soutenance 
- validation librables

### Updated
- 

## 2024-03-15


### Updated
- Add Black Isort to reqs
- Format code with black and isort
- Add small comments

### Todo
- change detroy => update
- Add update views
- Implement all CRUD Rules 
- Swagger Doc update all views



        try:
            user = CustomUser.objects.get(pk=pk)
            if (request.user == user):
                serializer = CustomUserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {
                        "error": "Vous n'êtes pas autorisé à mettre à jour cet utilisateur."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except ObjectDoesNotExist:
            return Response(
                {"error": "L'utilisateur n'existe pas"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
