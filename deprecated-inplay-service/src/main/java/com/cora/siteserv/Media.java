//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.21 at 03:30:49 PM CEST 
//


package com.cora.siteserv;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.datatype.XMLGregorianCalendar;


/**
 * <p>Java class for Media complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Media">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="refRecordId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="refRecordType" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="accessProperties" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="startTime" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="endTime" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="availableInCountries" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="isActive" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="url" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Media")
public class Media {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "refRecordId")
    protected String refRecordId;
    @XmlAttribute(name = "refRecordType")
    protected String refRecordType;
    @XmlAttribute(name = "accessProperties")
    protected String accessProperties;
    @XmlAttribute(name = "siteChannels")
    protected String siteChannels;
    @XmlAttribute(name = "startTime")
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar startTime;
    @XmlAttribute(name = "endTime")
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar endTime;
    @XmlAttribute(name = "isDisplayed")
    protected String isDisplayed;
    @XmlAttribute(name = "availableInCountries")
    protected String availableInCountries;
    @XmlAttribute(name = "isActive")
    protected String isActive;
    @XmlAttribute(name = "url")
    protected String url;

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
     * Gets the value of the refRecordId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRefRecordId() {
        return refRecordId;
    }

    /**
     * Sets the value of the refRecordId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRefRecordId(String value) {
        this.refRecordId = value;
    }

    /**
     * Gets the value of the refRecordType property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRefRecordType() {
        return refRecordType;
    }

    /**
     * Sets the value of the refRecordType property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRefRecordType(String value) {
        this.refRecordType = value;
    }

    /**
     * Gets the value of the accessProperties property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAccessProperties() {
        return accessProperties;
    }

    /**
     * Sets the value of the accessProperties property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAccessProperties(String value) {
        this.accessProperties = value;
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

    /**
     * Gets the value of the startTime property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getStartTime() {
        return startTime;
    }

    /**
     * Sets the value of the startTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setStartTime(XMLGregorianCalendar value) {
        this.startTime = value;
    }

    /**
     * Gets the value of the endTime property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getEndTime() {
        return endTime;
    }

    /**
     * Sets the value of the endTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setEndTime(XMLGregorianCalendar value) {
        this.endTime = value;
    }

    /**
     * Gets the value of the isDisplayed property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsDisplayed() {
        return isDisplayed;
    }

    /**
     * Sets the value of the isDisplayed property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsDisplayed(String value) {
        this.isDisplayed = value;
    }

    /**
     * Gets the value of the availableInCountries property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAvailableInCountries() {
        return availableInCountries;
    }

    /**
     * Sets the value of the availableInCountries property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAvailableInCountries(String value) {
        this.availableInCountries = value;
    }

    /**
     * Gets the value of the isActive property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsActive() {
        return isActive;
    }

    /**
     * Sets the value of the isActive property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsActive(String value) {
        this.isActive = value;
    }

    /**
     * Gets the value of the url property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getUrl() {
        return url;
    }

    /**
     * Sets the value of the url property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setUrl(String value) {
        this.url = value;
    }

}
