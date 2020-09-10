# users_test_task
A lot of users profiles. Simple train project for rest and code.

Requirements: django.

## Urls
* /login - Login page.
* /register - Register page.
* /index - Page with all users registered in the system. Admin can change all users and himself but usual user can't (himself only).
* /logout - Logout link. Redirect to /login - Login page
* /delete/{int:user_id} - Delete user with specific id. Login required
* /change/{int:user_id} - Change user with specific id. Login required

