package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.controller.AbstractControllerTest;
import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestPrizeRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ContestPrizeService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgImageParser;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.AdditionalAnswers;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

@WebMvcTest(
    value = {
      ContestPrizeController.class,
      ContestPrizeService.class,
    })
@AutoConfigureMockMvc(addFilters = false)
public class ContestPrizeControllerTest extends AbstractControllerTest {

  @MockBean private ContestPrizeRepository repository;
  @MockBean private ImageService imageService;
  @MockBean private SvgImageParser svgImageParser;
  private ContestPrize prizes;
  private List<ContestPrize> contestPrizes;
  private String path = "/images/uploads/svg";

  @Before
  public void init() {
    prizes = createPrizes();
    contestPrizes = getContestByContestId();
    given(repository.findByContestId(any(String.class))).willReturn(contestPrizes);
    given(repository.save(any(ContestPrize.class))).will(AdditionalAnswers.returnsFirstArg());
    given(repository.findById(any(String.class))).willReturn(Optional.of(prizes));
  }

  @Test
  public void testGetByContestId() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contestprize/2")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.[1].id", is("1")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateContestPrizes() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.post("/v1/api/contestprize")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(prizes)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateContest() throws Exception {

    this.mockMvc
        .perform(
            MockMvcRequestBuilders.put("/v1/api/contestprize/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TestUtil.convertObjectToJsonBytes(prizes)))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeletePrize() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/contestprize/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testReadOne() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.get("/v1/api/contestprize/prizeid/1")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id", is("1")))
        .andExpect(jsonPath("$.brand", is("coral")))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void uploadPrizeLogo() throws Exception {

    final MockMultipartFile file =
        new MockMultipartFile("file", "android.svg", "image/svg", "file".getBytes());
    given(repository.findById("1")).willReturn(Optional.of(prizes));
    given(imageService.upload(anyString(), any(), eq(path)))
        .willReturn(Optional.of(getFilename("android.svg", "323566.svg")));
    Svg svg = new Svg();
    svg.setSvg("<svg>");
    given(svgImageParser.parse(any())).willReturn(Optional.of(svg));
    this.mockMvc
        .perform(
            multipart("/v1/api/contestprize/1/file")
                .file("iconFile", file.getBytes())
                .content(TestUtil.convertObjectToJsonBytes(prizes)))
        .andExpect(status().is2xxSuccessful());

    Assert.assertNotNull(prizes.getIcon());
    Assert.assertEquals("android.svg", prizes.getIcon().getOriginalname());
    Assert.assertEquals("323566.svg", prizes.getIcon().getFilename());
  }

  @Test
  public void deleteImage() throws Exception {
    this.mockMvc
        .perform(
            MockMvcRequestBuilders.delete("/v1/api/contestprize/1/file?imageType=SIGHPOSTINGFILE")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  private static ContestPrize createPrizes() {
    ContestPrize prizes = new ContestPrize();
    prizes.setId("1");
    prizes.setContestId("2");
    prizes.setType("Cash");
    prizes.setIcon(getFilename("android.svg", "323566.svg"));
    prizes.setSignPosting(getFilename("android.svg", "323566.svg"));
    prizes.setBrand("coral");
    prizes.setNumberOfEntries("1-100");
    prizes.setValue("5.00");
    return prizes;
  }

  private static List<ContestPrize> getContestByContestId() {
    List<ContestPrize> contestPrizes = new ArrayList<>();
    ContestPrize prizes = new ContestPrize();
    prizes.setType("Cash");
    prizes.setIcon(getFilename("android.svg", "323566.svg"));
    prizes.setId("1");
    prizes.setBrand("coral");
    ContestPrize prizes1 = new ContestPrize();
    prizes1.setType("Cash");
    prizes1.setIcon(getFilename("android.svg", "323566.svg"));
    prizes1.setId("2");
    prizes1.setBrand("bma");
    contestPrizes.add(prizes1);
    contestPrizes.add(prizes);
    return contestPrizes;
  }

  private static Filename getFilename(String originalFN, String generatedFN) {
    Filename filename = new Filename();
    filename.setOriginalname(originalFN);
    filename.setFilename(generatedFN);
    filename.setPath("/test/path/");
    return filename;
  }
}
