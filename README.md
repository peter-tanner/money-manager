# Money manager

## I'm sick of using excel!

Personal money dashboard I made for myself. I will add more features when I need to, for example a journalling system or location server. I also anticipate adding a proper frontend to this app, to get over Django's admin interface limitations.

It's not the greatest code, since it tries to extend the django admin interface, which isn't designed for adding all of these features. For example, I want to make the charts show data from two tables, which required janking it in a way that is probably not how the library is meant to be used.

However, after searching for an hour I still think the Django admin interface is the most tightly integrated system for making a simple CRUD application. For example, if I were to use Django and an external frontend for the admin interface, I would need to add stuff like login which of course adds time, and to be honest I've had my fair share of CRUD apps this month. I also think most modern interfaces have way too much whitespace compared to the Django admin interface, which is nice and dense.
