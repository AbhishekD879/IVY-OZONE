package com.egalacoral.spark.timeform.tools;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class JavaDocGenerator {

  // @Test
  public void prepareHRMeetings() throws ParserConfigurationException, IOException, SAXException {
    process("javadoc/hr_meetings.xml");
  }

  // @Test
  public void prepareHRRaces() throws ParserConfigurationException, IOException, SAXException {
    process("javadoc/hr_races.xml");
  }

  // @Test
  public void prepareHREntries() throws ParserConfigurationException, IOException, SAXException {
    process("javadoc/hr_entries.xml");
  }

  public void process(String fileName)
      throws ParserConfigurationException, IOException, SAXException {
    DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
    Document document = builder.parse(getClass().getClassLoader().getResourceAsStream(fileName));
    Element table = document.getDocumentElement();
    Element header = child(child(table, "thead"), "tr");

    List<String> columns = new ArrayList<>();

    NodeList list = header.getElementsByTagName("th");
    for (int i = 0; i < list.getLength(); i++) {
      columns.add(list.item(i).getTextContent().trim());
    }
    Element body = child(table, "tbody");

    NodeList rows = body.getElementsByTagName("tr");
    for (int i = 0; i < rows.getLength(); i++) {
      Element row = (Element) rows.item(i);
      NodeList tds = row.getElementsByTagName("td");
      Element tdName = (Element) tds.item(0);
      tdName = child(tdName, "strong");
      String name = tdName.getTextContent().trim();

      System.out.println("\n" + name);
      System.out.println("  /**");
      for (int col = 1; col < tds.getLength(); col++) {
        Element td = (Element) tds.item(col);
        String val = td.getTextContent().trim();
        String colName = columns.get(col) + ": ";
        if ("Returns: ".equals(colName)) {
          colName = "@return ";
        } else if ("Summary: ".equals(colName)) {
          colName = "";
        }
        System.out.println("  * " + colName + val);
      }
      System.out.println("  * */");
    }
  }

  private Element child(Element from, String name) {
    return (Element) from.getElementsByTagName(name).item(0);
  }
}
