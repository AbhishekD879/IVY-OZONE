package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import java.io.IOException;
import java.util.Optional;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import org.junit.Before;
import org.junit.Test;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

public class SvgImageParserTest {

  private SvgImageParser svgImageParser;
  private DocumentBuilder builder;
  private Transformer transformer;
  private SvgImageOptimizer svgo;

  @Before
  public void before() throws Exception {
    builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
    transformer = TransformerFactory.newInstance().newTransformer();
    svgo = new SvgImageOptimizer(false);
    svgImageParser = new SvgImageParser(builder, transformer, svgo);
  }

  @Test
  public void testValidSVGImageParseWithBackward() throws Exception {

    MultipartFile file =
        new MockMultipartFile("svgName", TestUtil.readFromFile("service/valid.svg"));

    Optional<Svg> svg = svgImageParser.parse(file);

    assertTrue("SVG was returned", svg.isPresent());
    assertTrue("SVG id is present", svg.get().getId().length() > 1);
    assertTrue("SVG starts with #", svg.get().getId().startsWith("#"));
  }

  @Test
  public void testValidSVGImageParse() throws Exception {

    MultipartFile file =
        new MockMultipartFile("svgName", TestUtil.readFromFile("service/valid.svg"));

    Optional<Svg> svg = svgImageParser.parse(null, file, "");

    assertTrue("SVG was returned", svg.isPresent());
    assertTrue("SVG id is present", svg.get().getId().length() > 1);
    assertFalse("SVG does not start with #", svg.get().getId().startsWith("#"));
  }

  @Test
  public void testInvalidSVGImageParse() throws Exception {

    String svgText = "<svg>no root xml</svg>";
    MultipartFile file = new MockMultipartFile("svgName", svgText.getBytes());

    assertThrows(SvgImageParseException.class, () -> svgImageParser.parse(file));
  }

  @Test
  public void testValidSVGImageParseAndOptimized() throws Exception {

    MultipartFile file =
        new MockMultipartFile("svgName", TestUtil.readFromFile("service/valid.svg"));

    Optional<Svg> svg = svgImageParser.parse(null, file, "");

    assertTrue("SVG was returned", svg.isPresent());
    assertTrue("SVG id is present", svg.get().getId().length() > 1);
    assertFalse("SVG does not start with #", svg.get().getId().startsWith("#"));
  }

  @Test
  public void testValidSVGImageParseAndOverrideId() throws Exception {

    MultipartFile file =
        new MockMultipartFile("svgName", TestUtil.readFromFile("service/valid.svg"));

    String newId = "new-id-override";
    Optional<Svg> svg = svgImageParser.parse(newId, file, "");

    assertTrue("SVG was returned", svg.isPresent());
    assertTrue("SVG id is present", svg.get().getId().length() > 1);
    assertEquals("SVG starts contains newId", newId, svg.get().getId());
    assertTrue("SVG contains new id", svg.get().getSvg().contains(newId));
    assertTrue(
        "SVG should contain viewBox attribute",
        svg.get().getSvg().contains("viewBox=\"0 0 100 100\""));
  }

  @Test
  public void testNoViewBoxAttrInSVG() throws Exception {

    MultipartFile file =
        new MockMultipartFile("svgName", TestUtil.readFromFile("service/noViewbox.svg"));

    Optional<Svg> svg = svgImageParser.parse(file);

    assertTrue("SVG was returned", svg.isPresent());
    assertTrue(
        "SVG should contain generated viewBox attribute",
        svg.get().getSvg().contains("viewBox=\"5 10 300 100\""));
  }

  @Test
  public void testNoViewBoxAndWidthHeightAttrsInSVG() throws Exception {

    MultipartFile file =
        new MockMultipartFile("svgName", TestUtil.readFromFile("service/invalid.svg"));

    assertThrows(SvgImageParseException.class, () -> svgImageParser.parse(file));
  }

  @Test
  public void testDocumentConversion() throws IOException, SAXException {
    String svgContent =
        "<symbol id=\"8eb5115a-fae6-385e-935d-b7eeb039d97d\" viewBox=\"0 0 28 28\"> 8eb5115a-fae6-385e-935d-b7eeb039d97d\"as<defs xmlns=\"http://www.w3.org/2000/svg\">        <path d=\"M0 0h28v28H0z\" id=\"a\"/>    </defs>    <g  fill-rule=\"evenodd\" xmlns=\"http://www.w3.org/2000/svg\">        <mask  id=\"b\">            <use xmlns:xlink=\"http://www.w3.org/1999/xlink\" xlink:href=\"#a\"/>        </mask>        <g  mask=\"url(#b)\">            <path d=\"M16.102 13.641l.048.348a.883.883 0 0 0 .868.77h2.599l-3.098 11.389c-.074.27-.02.56.146.78a.87.87 0 0 0 .698.354h4.179a.85.85 0 0 0 .617-.258.923.923 0 0 0 .261-.637c-.005-.499-.398-.899-.877-.894h-3.025l3.096-11.389a.908.908 0 0 0-.147-.781.87.87 0 0 0-.698-.352H17.78L16.097.77a.882.882 0 0 0-.868-.77h-.98a.883.883 0 0 0-.869.77l-1.978 14.318c-.03.237.03.478.17.667.14.19.347.314.574.344a.88.88 0 0 0 .99-.76l.236-1.698h2.73zm-.297-2.154l-1.067-7.734-1.068 7.734h2.135z\"/>            <path d=\"M14.487 26.564a.371.371 0 0 1-.074-.007c-3.272-.696-6.077-2.639-7.9-5.468-3.752-5.83-2.105-13.654 3.67-17.442a.35.35 0 0 1 .488.105.36.36 0 0 1 .049.269.348.348 0 0 1-.153.222C5.117 7.818 3.564 15.2 7.104 20.701a11.707 11.707 0 0 0 7.455 5.16.356.356 0 0 1-.073.703\"/>            <path d=\"M11.725 28a.33.33 0 0 1-.298-.195.36.36 0 0 1 .15-.471l2.782-1.45a.319.319 0 0 1 .254-.018c.084.03.152.093.191.175a.359.359 0 0 1-.152.47l-2.78 1.452a.315.315 0 0 1-.147.036\"/>            <path d=\"M14.502 26.564a.336.336 0 0 1-.303-.194l-1.392-2.897a.356.356 0 0 1-.018-.264.339.339 0 0 1 .17-.199.332.332 0 0 1 .451.158l1.393 2.896a.35.35 0 0 1-.152.464.327.327 0 0 1-.149.036\"/>        </g>    </g></symbol>";
    Document document = svgImageParser.convertStringToDocument(svgContent);
    assertNotNull(document);
  }
}
