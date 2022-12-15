def if_is_in_fav_or_shop_list(self, obj, model):
    if (
        self.context.get('request') is not None
        and self.context.get('request').user.is_authenticated
    ):
        return model.objects.filter(
            user=self.context.get('request').user, recipe=obj
        ).exists()
    return False
