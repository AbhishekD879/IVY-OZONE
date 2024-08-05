//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.21 at 03:30:49 PM CEST 
//


package com.cora.siteserv;

import java.math.BigDecimal;
import java.math.BigInteger;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for Price complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Price">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isActive" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="displayOrder" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="outcomeVariantId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="priceType" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="priceNum" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="priceDen" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="priceDec" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="handicapValueDec" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obListOfStrings" />
 *       &lt;attribute name="rawHandicapValue" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="poolId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="poolType" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isToPlace" type="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}obBoolean" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Price")
public class Price {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "isActive")
    protected String isActive;
    @XmlAttribute(name = "displayOrder")
    protected BigInteger displayOrder;
    @XmlAttribute(name = "outcomeVariantId")
    protected String outcomeVariantId;
    @XmlAttribute(name = "priceType")
    protected String priceType;
    @XmlAttribute(name = "priceNum")
    protected BigInteger priceNum;
    @XmlAttribute(name = "priceDen")
    protected BigInteger priceDen;
    @XmlAttribute(name = "priceDec")
    protected BigDecimal priceDec;
    @XmlAttribute(name = "handicapValueDec")
    protected String handicapValueDec;
    @XmlAttribute(name = "rawHandicapValue")
    protected BigDecimal rawHandicapValue;
    @XmlAttribute(name = "poolId")
    protected String poolId;
    @XmlAttribute(name = "poolType")
    protected String poolType;
    @XmlAttribute(name = "isToPlace")
    protected String isToPlace;

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
     * Gets the value of the outcomeVariantId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeVariantId() {
        return outcomeVariantId;
    }

    /**
     * Sets the value of the outcomeVariantId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeVariantId(String value) {
        this.outcomeVariantId = value;
    }

    /**
     * Gets the value of the priceType property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPriceType() {
        return priceType;
    }

    /**
     * Sets the value of the priceType property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPriceType(String value) {
        this.priceType = value;
    }

    /**
     * Gets the value of the priceNum property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getPriceNum() {
        return priceNum;
    }

    /**
     * Sets the value of the priceNum property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setPriceNum(BigInteger value) {
        this.priceNum = value;
    }

    /**
     * Gets the value of the priceDen property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getPriceDen() {
        return priceDen;
    }

    /**
     * Sets the value of the priceDen property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setPriceDen(BigInteger value) {
        this.priceDen = value;
    }

    /**
     * Gets the value of the priceDec property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getPriceDec() {
        return priceDec;
    }

    /**
     * Sets the value of the priceDec property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setPriceDec(BigDecimal value) {
        this.priceDec = value;
    }

    /**
     * Gets the value of the handicapValueDec property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHandicapValueDec() {
        return handicapValueDec;
    }

    /**
     * Sets the value of the handicapValueDec property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHandicapValueDec(String value) {
        this.handicapValueDec = value;
    }

    /**
     * Gets the value of the rawHandicapValue property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getRawHandicapValue() {
        return rawHandicapValue;
    }

    /**
     * Sets the value of the rawHandicapValue property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setRawHandicapValue(BigDecimal value) {
        this.rawHandicapValue = value;
    }

    /**
     * Gets the value of the poolId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPoolId() {
        return poolId;
    }

    /**
     * Sets the value of the poolId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPoolId(String value) {
        this.poolId = value;
    }

    /**
     * Gets the value of the poolType property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPoolType() {
        return poolType;
    }

    /**
     * Sets the value of the poolType property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPoolType(String value) {
        this.poolType = value;
    }

    /**
     * Gets the value of the isToPlace property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsToPlace() {
        return isToPlace;
    }

    /**
     * Sets the value of the isToPlace property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsToPlace(String value) {
        this.isToPlace = value;
    }

}
