package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Post;
import com.ladbrokescoral.oxygen.cms.api.repository.PostRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class PostService extends AbstractService<Post> {

  @Autowired
  public PostService(PostRepository repository) {
    super(repository);
  }
}
