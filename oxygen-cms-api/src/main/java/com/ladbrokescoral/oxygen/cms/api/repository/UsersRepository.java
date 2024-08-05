package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.User;
import java.util.Optional;

public interface UsersRepository extends CustomMongoRepository<User> {

  Optional<User> findByEmailIgnoreCase(String email);
}
