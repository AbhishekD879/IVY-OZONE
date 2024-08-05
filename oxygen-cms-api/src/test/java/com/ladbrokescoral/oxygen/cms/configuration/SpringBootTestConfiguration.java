package com.ladbrokescoral.oxygen.cms.configuration;

import com.github.cloudyrock.spring.v5.MongockSpring5.MongockInitializingBeanRunner;
import com.ladbrokescoral.lib.autoconfigure.MasterSlaveConfigurationProperties;
import com.ladbrokescoral.oxygen.cms.Application;
import com.ladbrokescoral.oxygen.cms.api.repository.BigQueryQuestionEngineRepository;
import com.ladbrokescoral.oxygen.cms.api.scheduler.ScheduledTaskExecutor;
import com.ladbrokescoral.oxygen.cms.api.service.TimelineChangeListener;
import com.ladbrokescoral.oxygen.cms.api.service.interceptors.TimelineMongoEventListener;
import com.mongodb.client.MongoCollection;
import org.mockito.BDDMockito;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.data.mongo.MongoDataAutoConfiguration;
import org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mapping.context.MappingContext;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.convert.MongoConverter;
import org.springframework.data.mongodb.core.mapping.MongoPersistentEntity;

@Profile("UNIT")
@TestConfiguration
@Import(SecurityConfig.class)
@MockBean({
  BigQueryQuestionEngineRepository.class,
  TimelineChangeListener.class,
  TimelineMongoEventListener.class,
  ScheduledTaskExecutor.class,
  MasterSlaveConfigurationProperties.class,
  MongoCollection.class
}) // FIXME: MongoCollection see #TimelineChangelogRepositoryImpl
@EnableAutoConfiguration(exclude = {MongoAutoConfiguration.class, MongoDataAutoConfiguration.class})
public class SpringBootTestConfiguration extends BDDMockito {

  @Bean
  @Qualifier(Application.MONGOCK)
  public MongockInitializingBeanRunner mongockInitializingBeanRunner() {
    return mock(MongockInitializingBeanRunner.class);
  }

  @Bean
  public MongoTemplate mongoTemplate() {

    // FIXME: clean-up

    MongoTemplate mongoTemplate = mock(MongoTemplate.class);
    MongoConverter mongoConverter = mock(MongoConverter.class);
    MappingContext mappingContext = mock(MappingContext.class);
    MongoPersistentEntity mongoPersistentEntity = mock(MongoPersistentEntity.class);

    when(mongoPersistentEntity.getType()).thenReturn(Application.class);
    when(mappingContext.getRequiredPersistentEntity(any(Class.class)))
        .thenReturn(mongoPersistentEntity);
    when(mongoConverter.getMappingContext()).thenReturn(mappingContext);
    when(mongoTemplate.getConverter()).thenReturn(mongoConverter);

    return mongoTemplate;
  }
}
