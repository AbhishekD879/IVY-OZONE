//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.25 at 12:50:43 PM EEST 
//


package com.egalacoral.api.siteserv;

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for DrilldownTag complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="DrilldownTag">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;choice>
 *         &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}error" minOccurs="0"/>
 *         &lt;sequence>
 *           &lt;choice maxOccurs="unbounded" minOccurs="0">
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}drilldownTagLink"/>
 *           &lt;/choice>
 *         &lt;/sequence>
 *       &lt;/choice>
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="localisableName" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="lang" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "DrilldownTag", propOrder = {
    "error",
    "drilldownTagLink"
})
public class DrilldownTag {

    protected Error error;
    protected List<DrilldownTagLink> drilldownTagLink;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String name;
    @XmlAttribute
    protected String localisableName;
    @XmlAttribute
    protected String lang;
    @XmlAttribute
    protected String siteChannels;

    /**
     * Gets the value of the error property.
     * 
     * @return
     *     possible object is
     *     {@link Error }
     *     
     */
    public Error getError() {
        return error;
    }

    /**
     * Sets the value of the error property.
     * 
     * @param value
     *     allowed object is
     *     {@link Error }
     *     
     */
    public void setError(Error value) {
        this.error = value;
    }

    /**
     * Gets the value of the drilldownTagLink property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the drilldownTagLink property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getDrilldownTagLink().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link DrilldownTagLink }
     * 
     * 
     */
    public List<DrilldownTagLink> getDrilldownTagLink() {
        if (drilldownTagLink == null) {
            drilldownTagLink = new ArrayList<DrilldownTagLink>();
        }
        return this.drilldownTagLink;
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    /**
     * Gets the value of the name property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the value of the name property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setName(String value) {
        this.name = value;
    }

    /**
     * Gets the value of the localisableName property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLocalisableName() {
        return localisableName;
    }

    /**
     * Sets the value of the localisableName property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLocalisableName(String value) {
        this.localisableName = value;
    }

    /**
     * Gets the value of the lang property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLang() {
        return lang;
    }

    /**
     * Sets the value of the lang property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLang(String value) {
        this.lang = value;
    }

    /**
     * Gets the value of the siteChannels property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSiteChannels() {
        return siteChannels;
    }

    /**
     * Sets the value of the siteChannels property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSiteChannels(String value) {
        this.siteChannels = value;
    }

}
