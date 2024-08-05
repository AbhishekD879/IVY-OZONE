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
 * <p>Java class for Draw complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Draw">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="lotteryId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="sort" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isActive" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="drawDescriptionId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="description" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="openAtTime" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="shutAtTime" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="drawAtTime" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Draw")
public class Draw {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "lotteryId")
    protected String lotteryId;
    @XmlAttribute(name = "sort")
    protected String sort;
    @XmlAttribute(name = "isActive")
    protected String isActive;
    @XmlAttribute(name = "drawDescriptionId")
    protected String drawDescriptionId;
    @XmlAttribute(name = "description")
    protected String description;
    @XmlAttribute(name = "openAtTime")
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar openAtTime;
    @XmlAttribute(name = "shutAtTime")
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar shutAtTime;
    @XmlAttribute(name = "drawAtTime")
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar drawAtTime;

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
     * Gets the value of the lotteryId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLotteryId() {
        return lotteryId;
    }

    /**
     * Sets the value of the lotteryId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLotteryId(String value) {
        this.lotteryId = value;
    }

    /**
     * Gets the value of the sort property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSort() {
        return sort;
    }

    /**
     * Sets the value of the sort property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSort(String value) {
        this.sort = value;
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
     * Gets the value of the drawDescriptionId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDrawDescriptionId() {
        return drawDescriptionId;
    }

    /**
     * Sets the value of the drawDescriptionId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDrawDescriptionId(String value) {
        this.drawDescriptionId = value;
    }

    /**
     * Gets the value of the description property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDescription() {
        return description;
    }

    /**
     * Sets the value of the description property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDescription(String value) {
        this.description = value;
    }

    /**
     * Gets the value of the openAtTime property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getOpenAtTime() {
        return openAtTime;
    }

    /**
     * Sets the value of the openAtTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setOpenAtTime(XMLGregorianCalendar value) {
        this.openAtTime = value;
    }

    /**
     * Gets the value of the shutAtTime property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getShutAtTime() {
        return shutAtTime;
    }

    /**
     * Sets the value of the shutAtTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setShutAtTime(XMLGregorianCalendar value) {
        this.shutAtTime = value;
    }

    /**
     * Gets the value of the drawAtTime property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getDrawAtTime() {
        return drawAtTime;
    }

    /**
     * Sets the value of the drawAtTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setDrawAtTime(XMLGregorianCalendar value) {
        this.drawAtTime = value;
    }

}