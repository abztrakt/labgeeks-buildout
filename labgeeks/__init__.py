from south.signals import post_migrate


def update_permissions(**kwargs):
    import sys
    sys.stdout.write("If there are new content types or permissions added, remember to run-> labgeeks update_permissions\n\n")


post_migrate.connect(update_permissions)
