# **`BundleJoy`**
*A fun way to share our Joy*


---
 <br />
 
### `What is it?`
BundleJoy is a social site that is designed for sharing our precious bundles of joy with each other. While sharing we are able to also comment on those that bring others joy.


### `Technologies Used`
* Django
* Postgres
* Bootstrap
* S3  Bucket for Static

### Installation

Fork and clone the repository
Follow the commands below

```zsh
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

### Starting the App

```zsh
python manage.py runserver
```

Go to 127.0.0.1:8000 in your browser

Create an account and try it out

### Testing

```zsh
python manage.py test
```

### Deployment

BundleJoy is deployed at: [BundleJoy](https://bundlejoy-16d2631b52d2.herokuapp.com/)


## Code Snippets
<details>

<summary> Comment View </summary>


```Python
def comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        # A Form for a Comment Model
        if request.method == 'POST':
            comment = request.POST['comment']
            post.comments.create(user=request.user, body=comment, date_added=timezone.now())
            messages.success(request, f'Comment added successfully!')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        messages.success(request, f'You must be logged in to add comments.')
        return redirect('home')
```


</details>

<details>
<summary>Custom Filters</summary>

 filter to parse URL's entered into the profile. If the url is a complete url it will return the url, otherwise it will add https:// in front

```Python
from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def ensure_scheme(url):
    parsed = urlparse(url)
    if parsed.scheme:
        return url
    else:
        return 'https://' + url
```
</details>

