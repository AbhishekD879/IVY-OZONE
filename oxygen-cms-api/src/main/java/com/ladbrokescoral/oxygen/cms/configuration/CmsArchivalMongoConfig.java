package com.ladbrokescoral.oxygen.cms.configuration;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableMongoRepositories(
    basePackages = "com.ladbrokescoral.oxygen.cms.api.archival.repository",
    mongoTemplateRef = "cmsArchivalMongoTemplate")
@Profile("!UNIT")
public class CmsArchivalMongoConfig {}
