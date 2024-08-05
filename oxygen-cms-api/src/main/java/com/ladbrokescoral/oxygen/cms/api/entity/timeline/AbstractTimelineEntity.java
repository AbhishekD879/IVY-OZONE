package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import java.util.Optional;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;

public class AbstractTimelineEntity<T extends AbstractEntity> extends AbstractEntity {

  // FIXME: remove it. seems obsolete. already defined by #CreatedBy in #AbstractEntity
  @SuppressWarnings("unchecked")
  public final T prepareModelBeforeSave() {
    this.setId(null);
    String loggedUserId =
        Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .filter(Authentication::isAuthenticated)
            .map(Authentication::getPrincipal)
            .map(User.class::cast)
            .map(User::getId)
            .orElse(null);
    this.setCreatedBy(loggedUserId);
    this.setUpdatedBy(loggedUserId);
    return (T) this;
  }

  // FIXME: remove it. seems obsolete. already defined by #LastModifiedBy in #AbstractEntity
  @SuppressWarnings("unchecked")
  public T prepareModelBeforeUpdate() {
    String loggedUserId =
        Optional.ofNullable((SecurityContextHolder.getContext().getAuthentication()))
            .filter(Authentication::isAuthenticated)
            .map(Authentication::getPrincipal)
            .map(User.class::cast)
            .map(User::getId)
            .orElse(null);
    this.setUpdatedBy(loggedUserId);
    return (T) this;
  }
}
