package com.ladbrokescoral.oxygen.questionengine.integrationtest.config;

import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBMapper;
import com.ladbrokescoral.oxygen.questionengine.repository.AwardFailureRepository;
import com.ladbrokescoral.oxygen.questionengine.repository.UserAnswerRepository;
import org.socialsignin.spring.data.dynamodb.core.DynamoDBTemplate;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.TestPropertySource;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD})
@ActiveProfiles(profiles = "INTEGRATION-TEST")
@TestPropertySource(locations = "classpath:integration-test.properties")
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@MockBean(UserAnswerRepository.class)
@MockBean(AwardFailureRepository.class)
@MockBean(DynamoDBMapper.class)
@MockBean(AmazonDynamoDB.class)
@MockBean(DynamoDBTemplate.class)
public @interface IntegrationTest {
}
