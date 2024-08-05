//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.21 at 03:30:49 PM CEST 
//


package com.cora.siteserv;

import java.math.BigInteger;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for SubType complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="SubType">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="typeId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="displayOrder" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="drilldownTagNames" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="hasOpenEvent" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="cashoutAvail" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "SubType")
public class SubType {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "typeId")
    protected String typeId;
    @XmlAttribute(name = "name")
    protected String name;
    @XmlAttribute(name = "displayOrder")
    protected BigInteger displayOrder;
    @XmlAttribute(name = "drilldownTagNames")
    protected String drilldownTagNames;
    @XmlAttribute(name = "hasOpenEvent")
    protected String hasOpenEvent;
    @XmlAttribute(name = "isDisplayed")
    protected String isDisplayed;
    @XmlAttribute(name = "cashoutAvail")
    protected String cashoutAvail;

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
     * Gets the value of the typeId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTypeId() {
        return typeId;
    }

    /**
     * Sets the value of the typeId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTypeId(String value) {
        this.typeId = value;
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
     * Gets the value of the displayOrder property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getDisplayOrder() {
        return displayOrder;
    }

    /**
     * Sets the value of the displayOrder property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setDisplayOrder(BigInteger value) {
        this.displayOrder = value;
    }

    /**
     * Gets the value of the drilldownTagNames property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDrilldownTagNames() {
        return drilldownTagNames;
    }

    /**
     * Sets the value of the drilldownTagNames property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDrilldownTagNames(String value) {
        this.drilldownTagNames = value;
    }

    /**
     * Gets the value of the hasOpenEvent property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasOpenEvent() {
        return hasOpenEvent;
    }

    /**
     * Sets the value of the hasOpenEvent property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasOpenEvent(String value) {
        this.hasOpenEvent = value;
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
     * Gets the value of the cashoutAvail property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCashoutAvail() {
        return cashoutAvail;
    }

    /**
     * Sets the value of the cashoutAvail property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCashoutAvail(String value) {
        this.cashoutAvail = value;
    }

}
