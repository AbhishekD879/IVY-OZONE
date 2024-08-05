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
 * <p>Java class for DeadHeatReduction complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="DeadHeatReduction">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eachWayTermId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="factorNum" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="factorDen" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="typeCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "DeadHeatReduction")
public class DeadHeatReduction {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "eachWayTermId")
    protected String eachWayTermId;
    @XmlAttribute(name = "factorNum")
    protected BigInteger factorNum;
    @XmlAttribute(name = "factorDen")
    protected BigInteger factorDen;
    @XmlAttribute(name = "typeCode")
    protected String typeCode;

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
     * Gets the value of the eachWayTermId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEachWayTermId() {
        return eachWayTermId;
    }

    /**
     * Sets the value of the eachWayTermId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEachWayTermId(String value) {
        this.eachWayTermId = value;
    }

    /**
     * Gets the value of the factorNum property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getFactorNum() {
        return factorNum;
    }

    /**
     * Sets the value of the factorNum property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setFactorNum(BigInteger value) {
        this.factorNum = value;
    }

    /**
     * Gets the value of the factorDen property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getFactorDen() {
        return factorDen;
    }

    /**
     * Sets the value of the factorDen property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setFactorDen(BigInteger value) {
        this.factorDen = value;
    }

    /**
     * Gets the value of the typeCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getTypeCode() {
        return typeCode;
    }

    /**
     * Sets the value of the typeCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setTypeCode(String value) {
        this.typeCode = value;
    }

}
