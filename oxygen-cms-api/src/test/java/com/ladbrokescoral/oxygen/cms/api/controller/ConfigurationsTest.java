package com.ladbrokescoral.oxygen.cms.api.controller;

import static com.ladbrokescoral.oxygen.cms.api.controller.ApiConstants.PRIVATE_API;
import static org.mockito.AdditionalAnswers.returnsFirstArg;
import static org.mockito.AdditionalAnswers.returnsLastArg;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.Configurations;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.service.AuthenticationService;
import com.ladbrokescoral.oxygen.cms.api.service.ConfigsService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

@RunWith(SpringRunner.class)
@WebMvcTest({Configurations.class, AuthenticationService.class})
@AutoConfigureMockMvc(addFilters = false)
public class ConfigurationsTest {

  @Autowired private MockMvc mockMvc;

  @MockBean private ConfigsService configsService;
  @MockBean private UserService userService;

  private String brand = "bma";

  @Test
  public void testCreateElementIfElementWithSuchNameAlreadyExist() throws Exception {
    SystemConfiguration config = new SystemConfiguration();
    config.setBrand("bma");
    config.setId("NewElement");
    config.setName("NewElement");
    config.setProperties(new ArrayList<>());
    given(configsService.findElementByBrandAndName("bma", "NewElement"))
        .willReturn(Optional.of(config));
    mockMvc
        .perform(
            post(PRIVATE_API + "/configuration/brand/bma/element")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"NewElement\", \"items\":[]}"))
        .andExpect(status().isConflict());
  }

  @Test
  public void testCreateElementSuccessful() throws Exception {
    given(configsService.findElementByBrandAndName("bma", "NewElement"))
        .willReturn(Optional.empty());
    given(configsService.prepareModelBeforeSave(any())).will(returnsFirstArg());
    given(configsService.save(any(SystemConfiguration.class))).will(returnsFirstArg());
    mockMvc
        .perform(
            post(PRIVATE_API + "/configuration/brand/bma/element")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"NewElement\", \"items\":[]}"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testUpdateElementIfElementNotExist() throws Exception {
    given(configsService.findOne("NewElement")).willReturn(Optional.empty());

    mockMvc
        .perform(
            put(PRIVATE_API + "/configuration/brand/bma/element/NewElement")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testUpdateElementSuccessful() throws Exception {
    SystemConfiguration config = new SystemConfiguration();
    config.setBrand("bma");
    config.setId("NewElement");
    config.setName("NewElement");
    config.setProperties(new ArrayList<>());
    given(configsService.findOne("NewElement")).willReturn(Optional.of(config));
    given(configsService.update(any(), any())).will(returnsLastArg());

    mockMvc
        .perform(
            put(PRIVATE_API + "/configuration/brand/bma/element/NewElement")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"NewElement\", \"items\":[]}"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testDeleteElementIfElementNotExist() throws Exception {
    given(configsService.findOne("NewElement")).willReturn(Optional.empty());

    mockMvc
        .perform(
            delete(PRIVATE_API + "/configuration/brand/bma/element/NewElement")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
        .andExpect(status().isNotFound());
  }

  @Test
  public void testDeleteElementSuccessful() throws Exception {
    SystemConfiguration config = new SystemConfiguration();
    config.setBrand("bma");
    config.setId("NewElement");
    config.setName("NewElement");
    config.setProperties(new ArrayList<>());
    given(configsService.findOne("NewElement")).willReturn(Optional.of(config));

    mockMvc
        .perform(
            delete(PRIVATE_API + "/configuration/brand/bma/element/NewElement")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
  }

  @Test
  public void testCreateSuccessful() throws Exception {
    given(configsService.prepareModelBeforeSave(any())).will(returnsFirstArg());
    given(configsService.save(any(SystemConfiguration.class))).will(returnsFirstArg());
    mockMvc
        .perform(
            post(PRIVATE_API + "/configuration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"brand\": \"newBrand\","
                        + " \"config\": [{\"name\": \"NewElement\", \"items\":[]}]}"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void testCreateDuplicateError() throws Exception {
    given(configsService.prepareModelBeforeSave(any())).will(returnsFirstArg());
    given(configsService.save(any(SystemConfiguration.class)))
        .willThrow(new BadRequestException("Duplicate"));
    mockMvc
        .perform(
            post(PRIVATE_API + "/configuration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"brand\": \"newBrand\","
                        + " \"config\": [{\"name\": \"NewElement\", \"items\":[]}]}"))
        .andExpect(status().is4xxClientError());
  }

  @Test
  public void testCreateDuplicateOverwite() throws Exception {
    SystemConfiguration config = createConfig("bma", "NewElement");
    config.setOverwrite(true);
    given(configsService.prepareModelBeforeSave(any())).will(returnsFirstArg());
    given(configsService.findOne(any())).willReturn(Optional.of(config));
    given(configsService.findElementByBrandAndName(any(), any())).willReturn(Optional.of(config));
    given(configsService.update(any(), any())).will(returnsFirstArg());

    mockMvc
        .perform(
            post(PRIVATE_API + "/configuration")
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"brand\": \"newBrand\","
                        + " \"config\": [{\"name\": \"NewElement\", \"overwrite\": \"true\",\"items\":[]}]}"))
        .andExpect(status().is2xxSuccessful());
  }

  @Test
  public void getAll() throws Exception {
    given(configsService.findAll())
        .willReturn(
            Arrays.asList(
                createConfig(brand, "Config1"),
                createConfig(brand, "Config2"),
                createConfig("lb", "Config2"),
                createConfig("rf", "Config3")));
    mockMvc
        .perform(get(PRIVATE_API + "/configuration").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(
            content()
                .json(
                    "[\n"
                        + "{\"brand\": \"bma\", \"config\": [\n"
                        + "    {\"name\": \"Config1\", \"items\": []},\n"
                        + "    {\"name\": \"Config2\", \"items\": []}]}, \n"
                        + "{\"brand\": \"lb\", \"config\": [{\"name\": \"Config2\", \"items\": []}]}, \n"
                        + "  {\"brand\": \"rf\", \"config\": [{\"name\": \"Config3\", \"items\": []}]}]"));
  }

  @Test
  public void findByBrand() throws Exception {
    given(configsService.findByBrand(brand))
        .willReturn(Arrays.asList(createConfig(brand, "Config1"), createConfig(brand, "Config2")));
    mockMvc
        .perform(
            get(PRIVATE_API + "/configuration/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().is2xxSuccessful())
        .andExpect(
            content()
                .json(
                    "{\"brand\": \"bma\", \"config\": ["
                        + "{\"name\": \"Config1\", \"items\": []},"
                        + " {\"name\": \"Config2\", \"items\": []}"
                        + "]}"));
  }

  @Test
  public void testNotFoundExceptionWhenFindByBrand() throws Exception {
    given(configsService.findByBrand(brand)).willReturn(Collections.emptyList());
    mockMvc
        .perform(
            get(PRIVATE_API + "/configuration/brand/bma").contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  public void deleteAllByBrand() throws Exception {
    mockMvc
        .perform(
            delete(PRIVATE_API + "/configuration/brand/bma")
                .contentType(MediaType.APPLICATION_JSON))
        .andExpect(status().isNoContent());
    verify(configsService).deleteAllByBrand("bma");
  }

  private SystemConfiguration createConfig(String brand, String name) {
    SystemConfiguration config = new SystemConfiguration();
    config.setBrand(brand);
    config.setName(name);
    config.setProperties(Collections.emptyList());
    return config;
  }
}
