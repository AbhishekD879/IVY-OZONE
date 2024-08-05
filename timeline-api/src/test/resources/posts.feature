Feature: Posts
  Scenario: FE Client should get a "new post" notification when it's created on CMS
    Given FE client has an opened websocket connection
    When a post is created on CMS
    Then client gets notification about that

  Scenario: FE Client should get a "post has been removed" notification when it's unpublished on CMS
    Given FE client has an opened websocket connection
    When a post is unpublished on CMS
    Then client gets notification about that