//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.25 at 12:50:43 PM EEST 
//


package com.egalacoral.api.siteserv;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for NcastDividend complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="NcastDividend">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="marketId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="type" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="dividend" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="runnerNumbers" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "NcastDividend")
public class NcastDividend {

    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String marketId;
    @XmlAttribute
    protected String isDisplayed;
    @XmlAttribute
    protected String siteChannels;
    @XmlAttribute
    protected String type;
    @XmlAttribute
    protected BigDecimal dividend;
    @XmlAttribute
    protected String runnerNumbers;

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
     * Gets the value of the marketId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getMarketId() {
        return marketId;
    }

    /**
     * Sets the value of the marketId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setMarketId(String value) {
        this.marketId = value;
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
     * Gets the value of the type property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getType() {
        return type;
    }

    /**
     * Sets the value of the type property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setType(String value) {
        this.type = value;
    }

    /**
     * Gets the value of the dividend property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getDividend() {
        return dividend;
    }

    /**
     * Sets the value of the dividend property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setDividend(BigDecimal value) {
        this.dividend = value;
    }

    /**
     * Gets the value of the runnerNumbers property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRunnerNumbers() {
        return runnerNumbers;
    }

    /**
     * Sets the value of the runnerNumbers property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRunnerNumbers(String value) {
        this.runnerNumbers = value;
    }

}