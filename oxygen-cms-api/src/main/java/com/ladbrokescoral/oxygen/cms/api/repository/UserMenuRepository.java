package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.UserMenu;

public interface UserMenuRepository
    extends CustomMongoRepository<UserMenu>, FindByRepository<UserMenu> {}
