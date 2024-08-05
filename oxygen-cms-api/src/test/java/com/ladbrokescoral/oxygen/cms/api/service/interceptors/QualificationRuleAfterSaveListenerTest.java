package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.QualificationRuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QualificationRulePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class QualificationRuleAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<QualificationRule> {

  @Mock private QualificationRulePublicService service;
  @Getter @InjectMocks private QualificationRuleAfterSaveListener listener;

  @Getter @Mock private QualificationRule entity;
  @Getter @Mock private QualificationRuleDto qualificationRuleDto;
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Getter private List<?> collection = null;

  @Getter
  private Optional<QualificationRuleDto> qualificationRuledto =
      Optional.ofNullable(qualificationRuleDto);

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "qualification-rule"},
          {"connect", "api/connect", "qualification-rule"}
        });
  }

  @Before
  public void init() {

    ReflectionTestUtils.setField(listener, "ladsQualificationRuleTopic", "cms-qualification-rule");
    given(service.findByBrand(anyString())).willReturn(qualificationRuledto);
  }
}
