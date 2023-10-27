from recipes.models import Subscribe


def check_subscribe(request, author):
    """Проверка подписки."""

    return (
        request.user.is_authenticated
        and Subscribe.objects.filter(user=request.user, author=author).exists()
    )
