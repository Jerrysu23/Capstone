# This file is responsible for setting up all configuration that is necessary for connecting and setting up
# our mongoDB database.
#
# author: Preston Peck
# version: Sept. 3, 2024

# Eventually I can setup a user account for everyone to connect with, for now we can just use my credentials.
mongodb_uri = "mongodb+srv://prestontpeck:mTQWCzC8TLiQGKJz@jobquerycluster.gdmmr.mongodb.net/?retryWrites=true&w=majority&appName=JobQueryCluster"


def get_mongodb_uri():
    """Returns the uri string for connecting to our mongoDB database"""

    return mongodb_uri