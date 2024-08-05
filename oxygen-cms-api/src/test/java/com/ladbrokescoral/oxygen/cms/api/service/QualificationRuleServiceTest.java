package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.eq;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.repository.QualificationRuleRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class QualificationRuleServiceTest {

  @Mock private QualificationRuleRepository repository;
  @Mock private ImageService imageService;
  private QualificationRuleService service;

  @Before
  public void setUp() {
    service =
        new QualificationRuleService(repository, imageService, "/test/blacklist/path/", "abcdefg");
  }

  @Test
  public void uploadEncodedBlacklistedUsers() throws Exception {
    MultipartFile file =
        new MockMultipartFile("users", TestUtil.readFromFile("service/game/users.csv"));

    Filename filename = new Filename();
    filename.setPath("/test/blacklist/path/bma");
    filename.setOriginalname("users.csv");
    filename.setFilename("users.csv");
    filename.setFiletype("text/csv");
    filename.setSize("268");

    when(imageService.upload(any(), any(), eq("/test/blacklist/path/bma"), eq("users"), any()))
        .thenReturn(Optional.of(filename));

    QualificationRule qualificationRule = getQualificationRule();
    when(repository.findOneByBrand("bma")).thenReturn(Optional.of(qualificationRule));

    service.uploadEncryptedBlacklistedUsers("bma", file);

    assertEquals("/test/blacklist/path/bma/users.csv", qualificationRule.getBlacklistedUsersPath());
  }

  @Test(expected = FileUploadException.class)
  public void uploadFailed() throws Exception {
    MultipartFile file =
        new MockMultipartFile("users", TestUtil.readFromFile("service/game/users.csv"));

    when(imageService.upload(any(), any(), eq("/test/blacklist/path/bma"), eq("users"), any()))
        .thenReturn(Optional.empty());

    service.uploadEncryptedBlacklistedUsers("bma", file);
  }

  private QualificationRule getQualificationRule() {
    QualificationRule qualificationRule = new QualificationRule();
    qualificationRule.setBrand("bma");
    return qualificationRule;
  }
}
