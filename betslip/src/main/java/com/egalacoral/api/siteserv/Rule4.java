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
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.datatype.XMLGregorianCalendar;


/**
 * <p>Java class for Rule4 complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Rule4">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="marketId" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="fromDate" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="toDate" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="deductionType" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="deduction" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="isActive" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="outcomeId" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="outcomeName" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="runnerNumber" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Rule4")
public class Rule4 {

    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected BigInteger marketId;
    @XmlAttribute
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar fromDate;
    @XmlAttribute
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar toDate;
    @XmlAttribute
    protected String deductionType;
    @XmlAttribute
    protected BigDecimal deduction;
    @XmlAttribute
    protected String isActive;
    @XmlAttribute
    protected BigInteger outcomeId;
    @XmlAttribute
    protected String outcomeName;
    @XmlAttribute
    protected BigInteger runnerNumber;

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
     *     {@link BigInteger }
     *     
     */
    public BigInteger getMarketId() {
        return marketId;
    }

    /**
     * Sets the value of the marketId property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setMarketId(BigInteger value) {
        this.marketId = value;
    }

    /**
     * Gets the value of the fromDate property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getFromDate() {
        return fromDate;
    }

    /**
     * Sets the value of the fromDate property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setFromDate(XMLGregorianCalendar value) {
        this.fromDate = value;
    }

    /**
     * Gets the value of the toDate property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getToDate() {
        return toDate;
    }

    /**
     * Sets the value of the toDate property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setToDate(XMLGregorianCalendar value) {
        this.toDate = value;
    }

    /**
     * Gets the value of the deductionType property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDeductionType() {
        return deductionType;
    }

    /**
     * Sets the value of the deductionType property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDeductionType(String value) {
        this.deductionType = value;
    }

    /**
     * Gets the value of the deduction property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getDeduction() {
        return deduction;
    }

    /**
     * Sets the value of the deduction property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setDeduction(BigDecimal value) {
        this.deduction = value;
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
     * Gets the value of the outcomeId property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getOutcomeId() {
        return outcomeId;
    }

    /**
     * Sets the value of the outcomeId property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setOutcomeId(BigInteger value) {
        this.outcomeId = value;
    }

    /**
     * Gets the value of the outcomeName property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeName() {
        return outcomeName;
    }

    /**
     * Sets the value of the outcomeName property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeName(String value) {
        this.outcomeName = value;
    }

    /**
     * Gets the value of the runnerNumber property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getRunnerNumber() {
        return runnerNumber;
    }

    /**
     * Sets the value of the runnerNumber property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setRunnerNumber(BigInteger value) {
        this.runnerNumber = value;
    }

}
