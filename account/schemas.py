import graphene
from graphene_django  import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from account.models import User 
from cms.models import Post, Story, Photo, Video


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field() # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    send_secondary_email_activation =  mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()
    remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()

class UserType(DjangoObjectType):
    class Meta:
        fields = ['username','id','first_name','last_name']
        model= User

class PostType(DjangoObjectType):
    class Meta:
        fields = '__all__'
        model = Post 

class StoryType(DjangoObjectType):
    class Meta:
        fields = '__all__'
        model = Story 

class PhotoType(DjangoObjectType):
    class Meta:
        fields = '__all__'
        model = Photo

class VideoType(DjangoObjectType):
    class Meta:
        fields = '__all__'
        model = Video 




class Query(UserQuery,MeQuery,graphene.ObjectType):
    post = graphene.Field(PostType)
    posts = graphene.List(PostType)

    story = graphene.Field(StoryType)
    stories = graphene.List(StoryType)

    photo = graphene.Field(PhotoType)
    photos = graphene.List(PhotoType)

    video = graphene.Field(VideoType)
    videos = graphene.List(VideoType)

    def resolve_post(root, info, id):
        return Post.objects.get(id=id)

    def resolve_posts(root, info):
        return Post.objects.all()

    def resolve_story(root, info, id):
        return Story.objects.get(id=id)

    def resolve_stories(root, info):
        return Story.objects.all()

    def resolve_photo(root, info, id):
        return Photo.objects.get(id=id)

    def resolve_photos(root, info):
        return Photo.objects.all()

    def resolve_video(root, info, id):
        return Video.objects.get(id=id)

    def resolve_videos(root, info):
        return Video.objects.all()


class CreateStory(graphene.Mutation):
    story = graphene.Field(StoryType)

    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    @classmethod 
    def mutate(cls, info, root, title, body):
        return CreateStory(story = Story.objects.create(
            title= title,
            body = body,
            owner = info.context.user
        ))
class UpdateStory(graphene.Mutation):
    story = graphine.Field(StoryType)

    class Arguments:
        title = graphene.String()
        body = graphene.String()
    
    @classmethod 
    def mutate(cls, root, info, title, id, body):
        story = Story.objects.get(id=id, owner=info.context.user)
        story.title=title
        story.body=body 
        story.save()

        return UpdateStory(story=story)

class Mutations(AuthMutation,graphene.ObjectType):
    create_story = CreateStory.Field()
    update_story = UpdateStory.Field()





schema = graphene.Schema(query=Query, mutation=Mutations)