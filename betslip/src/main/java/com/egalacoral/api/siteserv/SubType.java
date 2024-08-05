//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.25 at 12:50:43 PM EEST 
//


package com.egalacoral.api.siteserv;

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
 *       &lt;attribute name="drilldownTagNames" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="hasOpenEvent" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
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

    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String typeId;
    @XmlAttribute
    protected String name;
    @XmlAttribute
    protected BigInteger displayOrder;
    @XmlAttribute
    protected String drilldownTagNames;
    @XmlAttribute
    protected String hasOpenEvent;
    @XmlAttribute
    protected String isDisplayed;
    @XmlAttribute
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
