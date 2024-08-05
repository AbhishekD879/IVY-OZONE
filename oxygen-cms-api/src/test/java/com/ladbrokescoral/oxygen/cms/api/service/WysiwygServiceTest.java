package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.WysiwygEntity;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.springframework.web.multipart.MultipartFile;

/** @author volodymyr.masliy on 26/03/2018 */
public class WysiwygServiceTest {

  private WysiwygService service;
  private ImageService imageService;

  @Before
  public void setUp() {
    imageService = Mockito.mock(ImageService.class);
    service = new WysiwygService(imageService, "core");
  }

  @Test
  public void testCorrectPathIsReturned() {
    MultipartFile mock = Mockito.mock(MultipartFile.class);
    Mockito.when(mock.getName()).thenReturn("file");
    Filename filename = new Filename();
    filename.setPath("path");
    filename.setFilename("filename");
    filename.setFullPath("https://akamai/path/filename");
    Mockito.when(
            imageService.upload(Mockito.anyString(), Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(Optional.of(filename));
    Optional<WysiwygEntity> col = service.attachWyswigImage("bma", mock, "col", "123");

    assertEquals("https://akamai/path/filename", col.get().getPath());
  }
}
