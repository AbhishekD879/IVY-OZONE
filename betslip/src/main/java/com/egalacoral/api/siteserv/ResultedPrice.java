//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.25 at 12:50:43 PM EEST 
//


package com.egalacoral.api.siteserv;

import java.math.BigDecimal;
import java.math.BigInteger;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for ResultedPrice complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="ResultedPrice">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="outcomeId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="priceTypeCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="priceNum" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="priceDen" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="priceDec" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="isToPlace" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "ResultedPrice")
public class ResultedPrice {

    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String outcomeId;
    @XmlAttribute
    protected String priceTypeCode;
    @XmlAttribute
    protected BigInteger priceNum;
    @XmlAttribute
    protected BigInteger priceDen;
    @XmlAttribute
    protected BigDecimal priceDec;
    @XmlAttribute
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
     * Gets the value of the outcomeId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeId() {
        return outcomeId;
    }

    /**
     * Sets the value of the outcomeId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeId(String value) {
        this.outcomeId = value;
    }

    /**
     * Gets the value of the priceTypeCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getPriceTypeCode() {
        return priceTypeCode;
    }

    /**
     * Sets the value of the priceTypeCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setPriceTypeCode(String value) {
        this.priceTypeCode = value;
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
