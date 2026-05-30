# Add Auth to a DRF Project

A **2-day assignment** (Wed Sep 2 + Sat Sep 5) — pick a DRF project you've already built and bolt on Django Token Auth.  By the end, every endpoint requires a token, and you have working signup + login routes that hand out tokens.

> The Saturday lesson is "Django Auth (continued)" — same project, continued work.  Don't try to finish everything Wednesday; this assignment is intentionally sized to span two evenings.

## Pick a DRF project

Any one of these works — pick the one that feels easiest to bring back online:
- Your **School API** stack from week 12-13 (you already have models + endpoints)
- The lesson's [drf-wine-api](https://github.com/CP-Evenings-and-Weekends/drf-wine-api)
- The [Article Publications](https://github.com/CP-Evenings-and-Weekends/article-publications) project from Mon Aug 24
- Your **Personal Project API Prototype** from this week
- Anything else with DRF + at least one endpoint

## Day-by-day plan

- **Wed Sep 2 (today)** — wire up token auth locally: add the `accounts` app, signup view, token endpoint, default permission classes.  Confirm with Postman that the API is locked down and your token works.
- **Sat Sep 5** — finish what you didn't get to: tests for the auth flow, ensuring the password isn't leaked in any response, polishing, and (if time) tying it into the deployed AWS instance from the Aug 29 lesson.

## Requirements

### 1. Add DRF Token Auth settings

In your project's `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',  # NEW — provides the Token model
    'accounts',                  # NEW — your new app (step 2)
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

Then run **`python manage.py migrate`** — `authtoken` creates a `Token` table you'll need.

### 2. Build the `accounts` app

```bash
python manage.py startapp accounts
```

Don't add anything to `accounts/models.py` — Django's built-in `User` model is what we want.

In `accounts/serializers.py` write a `SignupSerializer` that:
- Takes `username` and `password`
- Marks `password` as **`write_only=True`** so it's never echoed back in any response
- Uses `User.objects.create_user(...)` inside its `create()` method so the password gets hashed

In `accounts/views.py` write a `SignupView` (a DRF `CreateAPIView`) that uses your serializer and sets `permission_classes = [AllowAny]` (otherwise no one could ever sign up).

In `accounts/urls.py` wire two routes:
- `signup/` → your `SignupView`
- `get-token/` → DRF's built-in `obtain_auth_token`

Then include `accounts.urls` in your project `urls.py`.

### 3. Verify the full flow with Postman

1. `GET /<some_protected_endpoint>/` → expect `401 Unauthorized`
2. `POST /accounts/signup/` with `{"username": "...", "password": "..."}` → expect `201` (and confirm the response does **not** include the password)
3. `POST /accounts/get-token/` with the same credentials → expect a `{"token": "..."}` response
4. `GET /<some_protected_endpoint>/` again, this time with header `Authorization: Token <your_token>` → expect `200` with your data

### 4. (Saturday) Test the auth flow

Write tests covering:
- Unauthenticated requests get `401`
- Signup creates a user without exposing the password
- A valid token unlocks protected endpoints
- An invalid token still gets `401`

DRF's `APIClient` has `credentials(HTTP_AUTHORIZATION='Token ...')` for setting the header in tests.

## Things to think about
- Why **`write_only=True`** on the password field?  What happens if you forget it?  (Try it — every signup will echo the plaintext password back in the 201 response.)
- `User.objects.create_user(...)` vs `User.objects.create(...)` — what does the underscore version do that the plain one doesn't?  (Hint: `password` hashing.)
- DRF's `obtain_auth_token` returns a token that doesn't expire.  Is that OK?  Where would it bite you in production?  What's the standard fix?  (Hint: JWT, session timeouts, token rotation.)
- The default permission is `IsAuthenticated`.  What if you want **some** endpoints public and some not?  How would you mix per-view permissions with the global default?

## Stretch
- Add a **logout** endpoint that deletes the requesting user's token (forces the client to obtain a new one to keep using the API).
- Add an `is_staff` check so a delete endpoint only works for staff users.
- Add `password` validation (min length, no common-password check) — Django's built-in `validate_password` is what you want.
- After Saturday's deploy work, run the full auth flow against your AWS-deployed instance, not just localhost.

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!
