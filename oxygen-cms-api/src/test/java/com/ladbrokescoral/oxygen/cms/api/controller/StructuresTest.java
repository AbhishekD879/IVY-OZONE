package com.ladbrokescoral.oxygen.cms.api.controller;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Structures;
import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.web.multipart.MultipartFile;

@WebMvcTest({Structures.class})
@AutoConfigureMockMvc(addFilters = false)
public class StructuresTest extends AbstractControllerTest {

  @Autowired private MockMvc mockMvc;

  @MockBean private StructureService structureServiceMock;
  private StructureDto structure;

  @Before
  public void init() {
    structure = new StructureDto();
    structure.setBrand("bma");
    HashMap<String, Map<String, Object>> structure = new HashMap<>();
    structure.put("element", new HashMap<>());
    this.structure.setStructure(structure);
  }

  @Test
  public void testCreateElement() throws Exception {
    given(structureServiceMock.updateStructureItem(eq("1234"), eq("NewElement"), anyMap()))
        .willReturn(Optional.of(structure));
    Element element = new Element(UUID.randomUUID().toString(), 12);

    mockMvc
        .perform(
            put(PRIVATE_API + "/structure/1234/NewElement")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(element)))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.stringField", is(element.getStringField())))
        .andExpect(jsonPath("$.numberField", is(element.getNumberField())));
  }

  @Test
  public void testFindElement() throws Exception {
    Map<String, Object> element = new HashMap<>();
    element.put("stringField", "qwerty");
    element.put("numberField", 1);
    structure.getStructure().put("Element1", element);
    given(structureServiceMock.findByBrandAndConfigName("1234", "Element1"))
        .willReturn(Optional.of(element));

    mockMvc
        .perform(get(PRIVATE_API + "/structure/{id}/{elementName}", "1234", "Element1"))
        .andExpect(status().is2xxSuccessful())
        .andExpect(jsonPath("$.stringField", is("qwerty")))
        .andExpect(jsonPath("$.numberField", is(1)));
  }

  @Test
  public void testDeleteElement() throws Exception {
    structure.getStructure().put("Element1", Collections.singletonMap("qwerty", 1));
    given(structureServiceMock.resetToDefaultItem("1234", "Element1"))
        .willReturn(Optional.of(structure));

    mockMvc
        .perform(delete(PRIVATE_API + "/structure/{id}/{elementName}", "1234", "Element1"))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testDeleteNotExistingElement() throws Exception {
    given(structureServiceMock.resetToDefaultItem("1234", "Element1")).willReturn(Optional.empty());
    mockMvc
        .perform(delete(PRIVATE_API + "/structure/{id}/{elementName}", "1234", "Element1"))
        .andExpect(status().isNotFound());
  }

  @Test
  public void create() throws Exception {
    given(structureServiceMock.updateStructure(anyString(), eq(structure))).willReturn(structure);

    mockMvc
        .perform(
            post(PRIVATE_API + "/structure")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(structure)))
        .andExpect(status().isCreated());
  }

  @Test
  public void getAllStructures() throws Exception {
    mockMvc
        .perform(get(PRIVATE_API + "/structure").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());

    verify(structureServiceMock).findAllStructures();
  }

  @Test
  public void getByBrand() throws Exception {
    given(structureServiceMock.findStructureByBrand(eq("bma"))).willReturn(Optional.of(structure));

    mockMvc
        .perform(get(PRIVATE_API + "/structure/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getByBrandNotFound() throws Exception {
    given(structureServiceMock.findStructureByBrand(eq("bma"))).willReturn(Optional.empty());

    mockMvc
        .perform(get(PRIVATE_API + "/structure/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void update() throws Exception {
    mockMvc
        .perform(
            put(PRIVATE_API + "/structure/brand/bma")
                .contentType(MediaType.APPLICATION_JSON)
                .content(new ObjectMapper().writeValueAsString(structure)))
        .andExpect(status().is2xxSuccessful());

    verify(structureServiceMock).updateStructure(eq("bma"), eq(structure));
  }

  @Test
  public void deleteByBrand() throws Exception {
    mockMvc
        .perform(
            delete(PRIVATE_API + "/structure/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());

    verify(structureServiceMock).resetToDefaultForBrand(eq("bma"));
  }

  @Test
  public void uploadImage() throws Exception {
    given(
            structureServiceMock.uploadImage(
                eq("bma"), eq("element"), eq("property"), any(MultipartFile.class)))
        .willReturn(Optional.of("/path/image"));
    MockMultipartFile file =
        new MockMultipartFile("file", "filename.jpg", "image/jpg", "some xml".getBytes());

    mockMvc
        .perform(
            MockMvcRequestBuilders.multipart(
                    PRIVATE_API + "/structure/brand/bma/element/property/image")
                .file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void uploadImageFailed() throws Exception {
    given(
            structureServiceMock.uploadImage(
                eq("bma"), eq("element"), eq("property"), any(MultipartFile.class)))
        .willReturn(Optional.empty());
    MockMultipartFile file =
        new MockMultipartFile("file", "filename.jpg", "image/jpg", "some xml".getBytes());

    mockMvc
        .perform(
            MockMvcRequestBuilders.multipart(
                    PRIVATE_API + "/structure/brand/bma/element/property/image")
                .file(file))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void uploadSvg() throws Exception {
    given(
            structureServiceMock.uploadSvg(
                eq("bma"), eq("element"), eq("property"), any(MultipartFile.class)))
        .willReturn(Optional.of("/path/image"));
    MockMultipartFile file =
        new MockMultipartFile("file", "filename.svg", "image/svg", "some xml".getBytes());

    mockMvc
        .perform(
            MockMvcRequestBuilders.multipart(
                    PRIVATE_API + "/structure/brand/bma/element/property/svg")
                .file(file))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void uploadSvgFailed() throws Exception {
    given(
            structureServiceMock.uploadSvg(
                eq("bma"), eq("element"), eq("property"), any(MultipartFile.class)))
        .willReturn(Optional.empty());
    MockMultipartFile file =
        new MockMultipartFile("file", "filename.svg", "image/svg", "some xml".getBytes());

    mockMvc
        .perform(
            MockMvcRequestBuilders.multipart(
                    PRIVATE_API + "/structure/brand/bma/element/property/svg")
                .file(file))
        .andExpect(status().isBadRequest());
  }

  @Test
  public void removeImage() throws Exception {
    given(structureServiceMock.removeImage(eq("bma"), eq("element"), eq("property")))
        .willReturn(Optional.of(structure));

    mockMvc
        .perform(
            delete(PRIVATE_API + "/structure/brand/bma/element/property/image")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void removeImageFailed() throws Exception {
    given(structureServiceMock.removeImage(eq("bma"), eq("element"), eq("property")))
        .willReturn(Optional.empty());

    mockMvc
        .perform(
            delete(PRIVATE_API + "/structure/brand/bma/element/property/image")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  /**
   * This Element class is just for testing sake Structure object contains map of schemaless
   * elements
   */
  @Getter
  @AllArgsConstructor
  private static class Element {
    private String stringField;
    private Integer numberField;
  }
}
