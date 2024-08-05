package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

@Slf4j
@Service
public class SvgImageParser {

  private static final String SYMBOL_TAG = "symbol";
  private static final String ID_ATTRIBUTE = "id";
  private static final String SVG_TAG = "svg";
  private static final String VIEW_BOX_ATTR = "viewBox";
  private static final String WIDTH_ATTR = "width";
  private static final String HEIGHT_ATTR = "height";
  private static final String X_ATTR = "x";
  private static final String Y_ATTR = "y";
  private static final int FIRST_ITEM_INDEX = 0;

  private DocumentBuilder builder;
  private Transformer transformer;
  private SvgImageOptimizer svgImageOptimizer;

  @Autowired
  public SvgImageParser(
      DocumentBuilder builder, Transformer transformer, SvgImageOptimizer svgImageOptimizer) {
    this.builder = builder;
    this.transformer = transformer;
    this.svgImageOptimizer = svgImageOptimizer;
  }

  public Optional<Svg> parse(MultipartFile file) {
    return parse(null, file, "#");
  }

  public Optional<Svg> parse(String overrideSvgId, MultipartFile file) {
    return parse(null, file, "#");
  }

  public Optional<Svg> parse(String overrideSvgId, MultipartFile file, String svgIdPrefix) {
    Optional<String> optimizedImage = svgImageOptimizer.optimize(validateXML(file));
    if (optimizedImage.isPresent()) {
      return parse(overrideSvgId, file.getOriginalFilename(), optimizedImage.get(), svgIdPrefix);
    }
    return Optional.empty();
  }

  private String validateXML(MultipartFile svg) {
    try (InputStream is = svg.getInputStream()) {
      Document document = builder.parse(svg.getInputStream());
      Objects.requireNonNull(document);
      return toString(document);
    } catch (IOException | SAXException | TransformerException e) {
      log.error("Failed to validate svg file : ", e);
      throw new SvgImageParseException();
    }
  }

  private Optional<Svg> parse(
      String overrideSvgId, String filename, String svgString, String svgIdPrefix) {
    Svg svg = null;
    try (ByteArrayInputStream image = new ByteArrayInputStream(svgString.getBytes())) {
      Document document = builder.parse(image);
      Node symbolNode = getFirstNodeByTagName(document, SYMBOL_TAG);
      if (Objects.isNull(symbolNode)) {
        String uuid = UUID.nameUUIDFromBytes(filename.getBytes()).toString();
        symbolNode = createSymbolNode(document, uuid);
      }
      if (StringUtils.isNotBlank(overrideSvgId) && symbolNode instanceof Element) {
        ((Element) symbolNode).setAttribute(ID_ATTRIBUTE, overrideSvgId);
      }
      symbolNode.normalize();
      Node idNode = getAttributeNode(symbolNode, ID_ATTRIBUTE);

      svg = new Svg();
      svg.setSvg(toString(symbolNode));
      svg.setId(svgIdPrefix + idNode.getTextContent());
      svg.setValue(filename);

    } catch (SAXException | IOException e) {
      log.error("Error happened while parsing svg file : ", e);
    } catch (TransformerException e) {
      log.error("Error happened getting string 'symbol' node representation : ", e);
    }

    return Optional.ofNullable(svg);
  }

  public String toString(Node document) throws TransformerException {
    StringWriter writer = new StringWriter();
    transformer.transform(new DOMSource(document), new StreamResult(writer));
    return writer.getBuffer().toString();
  }

  private Node createSymbolNode(Document document, String uuid) {
    Element symbolNode = document.createElement(SYMBOL_TAG);
    symbolNode.setAttribute(ID_ATTRIBUTE, uuid);

    Node svgTagNode = getFirstNodeByTagName(document, SVG_TAG);
    Optional<String> viewBoxValue =
        Optional.ofNullable(getAttributeNode(svgTagNode, VIEW_BOX_ATTR)).map(Node::getNodeValue);
    Optional<String> widthValue =
        Optional.ofNullable(getAttributeNode(svgTagNode, WIDTH_ATTR)).map(Node::getNodeValue);
    Optional<String> heightValue =
        Optional.ofNullable(getAttributeNode(svgTagNode, HEIGHT_ATTR)).map(Node::getNodeValue);
    Optional<String> xValue =
        Optional.ofNullable(getAttributeNode(svgTagNode, X_ATTR)).map(Node::getNodeValue);
    Optional<String> yValue =
        Optional.ofNullable(getAttributeNode(svgTagNode, Y_ATTR)).map(Node::getNodeValue);

    viewBoxValue.ifPresent(vba -> symbolNode.setAttribute(VIEW_BOX_ATTR, vba));
    widthValue.ifPresent(wa -> symbolNode.setAttribute(WIDTH_ATTR, wa));
    heightValue.ifPresent(ha -> symbolNode.setAttribute(HEIGHT_ATTR, ha));

    if (!(viewBoxValue.isPresent() || (widthValue.isPresent() && heightValue.isPresent()))) {
      throw new SvgImageParseException();
    }

    // generate viewBox from x y width height
    if (!viewBoxValue.isPresent()) {
      int x = xValue.map(Integer::parseInt).orElse(0);
      int y = yValue.map(Integer::parseInt).orElse(0);
      int width = widthValue.map(Integer::parseInt).orElse(0);
      int height = heightValue.map(Integer::parseInt).orElse(0);
      String vbValue = String.format("%s %s %s %s", x, y, width, height);
      symbolNode.setAttribute(VIEW_BOX_ATTR, vbValue);
    }

    // always delete x y width height
    symbolNode.removeAttribute(WIDTH_ATTR);
    symbolNode.removeAttribute(HEIGHT_ATTR);
    symbolNode.removeAttribute(X_ATTR);
    symbolNode.removeAttribute(Y_ATTR);

    NodeList list = svgTagNode.getChildNodes();
    while (list.getLength() > FIRST_ITEM_INDEX) {
      symbolNode.appendChild(list.item(FIRST_ITEM_INDEX));
    }

    document.adoptNode(symbolNode);
    return symbolNode;
  }

  private Node getAttributeNode(Node symbolNode, String attributeName) {
    return symbolNode.getAttributes().getNamedItem(attributeName);
  }

  public Node getFirstNodeByTagName(Document document, String symbolTag) {
    return document.getElementsByTagName(symbolTag).item(FIRST_ITEM_INDEX);
  }

  public Document convertStringToDocument(String svgContent) throws SAXException, IOException {
    return builder.parse(new InputSource(new StringReader(svgContent)));
  }
}
