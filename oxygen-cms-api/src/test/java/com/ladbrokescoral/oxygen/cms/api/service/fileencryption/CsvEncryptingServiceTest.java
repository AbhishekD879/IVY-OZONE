package com.ladbrokescoral.oxygen.cms.api.service.fileencryption;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;

import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.service.fileencryption.CsvEncryptingService.EncryptedMultipartFile;
import java.io.IOException;
import org.assertj.core.api.BDDAssertions;
import org.junit.Before;
import org.junit.Test;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

public class CsvEncryptingServiceTest extends BDDAssertions {

  private MultipartFile original;
  private MultipartFile hashed;

  private CsvEncryptingService service;

  @Before
  public void setUp() throws Exception {
    original = new MockMultipartFile("users", TestUtil.readFromFile("service/game/users.csv"));
    hashed =
        new EncryptedMultipartFile(
            TestUtil.readFromFileAsBytes("service/game/users_hashed.csv"), original);

    service = new CsvEncryptingService(original, "abcdefg", getCsvSchema());
  }

  @Test
  public void testEncryptedFileInput() throws IOException {
    String encryptedFileInput = new String(service.getEncryptedContent().getBytes());

    assertThat(encryptedFileInput)
        .contains("3027f9bf6acb01234b53dc82efd6d1f9c2dd784b6e5bfe26ff1f4ea4422fc083")
        .contains("06dc459198b38d2014979f9c871d4c49a27289c14b7a6d6362e3dd3c17534674")
        .contains("4fa50cb793f81b6357f537dadd25200412e3344022ed71751bb75dbb3fcf4a38")
        .contains("9979281c5fc4af9c6d7639fd017b75cdd9923fd0f0dfafaaad3be7159922f7b7");
  }

  @Test
  public void testEncryptedCsvFile() {

    MultipartFile result = service.getEncryptedContent();

    assertEquals(hashed, result);
  }

  @Test
  public void testEmptyCsvFile() {
    MultipartFile empty = new MockMultipartFile("users", new byte[0]);
    service = new CsvEncryptingService(empty, "abcdefg", getCsvSchema());

    MultipartFile encryptedFileInput = service.getEncryptedContent();

    assertTrue(encryptedFileInput.isEmpty());
  }

  private CsvSchema getCsvSchema() {
    return CsvSchema.builder().build().withoutHeader();
  }
}
