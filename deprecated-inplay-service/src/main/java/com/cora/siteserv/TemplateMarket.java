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
 * <p>Java class for TemplateMarket complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="TemplateMarket">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="typeId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="displayOrder" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="marketMeaningMajorCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="marketMeaningMinorCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="dispSortId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="dispSortName" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="collectionIds" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="collectionNames" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="isGrouped" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "TemplateMarket")
public class TemplateMarket {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "typeId")
    protected String typeId;
    @XmlAttribute(name = "displayOrder")
    protected BigInteger displayOrder;
    @XmlAttribute(name = "siteChannels")
    protected String siteChannels;
    @XmlAttribute(name = "marketMeaningMajorCode")
    protected String marketMeaningMajorCode;
    @XmlAttribute(name = "marketMeaningMinorCode")
    protected String marketMeaningMinorCode;
    @XmlAttribute(name = "dispSortId")
    protected String dispSortId;
    @XmlAttribute(name = "dispSortName")
    protected String dispSortName;
    @XmlAttribute(name = "collectionIds")
    protected String collectionIds;
    @XmlAttribute(name = "collectionNames")
    protected String collectionNames;
    @XmlAttribute(name = "name")
    protected String name;
    @XmlAttribute(name = "isDisplayed")
    protected String isDisplayed;
    @XmlAttribute(name = "isGrouped")
    protected String isGrouped;

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
     * Gets the value of the marketMeaningMajorCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getMarketMeaningMajorCode() {
        return marketMeaningMajorCode;
    }

    /**
     * Sets the value of the marketMeaningMajorCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setMarketMeaningMajorCode(String value) {
        this.marketMeaningMajorCode = value;
    }

    /**
     * Gets the value of the marketMeaningMinorCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getMarketMeaningMinorCode() {
        return marketMeaningMinorCode;
    }

    /**
     * Sets the value of the marketMeaningMinorCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setMarketMeaningMinorCode(String value) {
        this.marketMeaningMinorCode = value;
    }

    /**
     * Gets the value of the dispSortId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDispSortId() {
        return dispSortId;
    }

    /**
     * Sets the value of the dispSortId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDispSortId(String value) {
        this.dispSortId = value;
    }

    /**
     * Gets the value of the dispSortName property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDispSortName() {
        return dispSortName;
    }

    /**
     * Sets the value of the dispSortName property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDispSortName(String value) {
        this.dispSortName = value;
    }

    /**
     * Gets the value of the collectionIds property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCollectionIds() {
        return collectionIds;
    }

    /**
     * Sets the value of the collectionIds property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCollectionIds(String value) {
        this.collectionIds = value;
    }

    /**
     * Gets the value of the collectionNames property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCollectionNames() {
        return collectionNames;
    }

    /**
     * Sets the value of the collectionNames property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCollectionNames(String value) {
        this.collectionNames = value;
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
     * Gets the value of the isGrouped property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsGrouped() {
        return isGrouped;
    }

    /**
     * Sets the value of the isGrouped property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsGrouped(String value) {
        this.isGrouped = value;
    }

}
