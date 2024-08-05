package com.ladbrokescoral.oxygen.timeline.api.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;

@Profile("!unit")
@Configuration
@EnableRedisRepositories
public class RedisConfig {}
