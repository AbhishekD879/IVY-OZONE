//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAnyAttribute;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.namespace.QName;


/**
 * <p>Java class for betType complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="betType">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="externalRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="errorRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="legRestrictions">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;attribute name="min" use="required" type="{http://schema.openbet.com/core}nonNegativeInt" />
 *                 &lt;attribute name="max" use="required" type="{http://schema.openbet.com/core}nonNegativeInt" />
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *         &lt;element name="line" maxOccurs="unbounded">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;attribute name="combination" use="required" type="{http://schema.products.sportsbook.openbet.com/bet}betLineCombination" />
 *                 &lt;attribute name="legs" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *       &lt;/sequence>
 *       &lt;attGroup ref="{http://schema.openbet.com/core}entityAttrGroup"/>
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="status" type="{http://schema.openbet.com/core}activeSuspended" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "betType", propOrder = {
    "externalRef",
    "errorRef",
    "legRestrictions",
    "line"
})
public class BetType
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    protected List<EntityRef> externalRef;
    protected List<EntityRef> errorRef;
    @XmlElement(required = true)
    protected LegRestrictions legRestrictions;
    @XmlElement(required = true)
    protected List<Line> line;
    @XmlAttribute
    protected String name;
    @XmlAttribute
    protected ActiveSuspended status;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String documentId;
    @XmlAttribute
    protected String provider;
    @XmlAttribute
    protected String addr;
    @XmlAttribute
    protected String version;
    @XmlAttribute
    @XmlSchemaType(name = "positiveInteger")
    protected BigInteger ordering;
    @XmlAnyAttribute
    private Map<QName, String> otherAttributes = new HashMap<QName, String>();

    /**
     * Gets the value of the externalRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the externalRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getExternalRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getExternalRef() {
        if (externalRef == null) {
            externalRef = new ArrayList<EntityRef>();
        }
        return this.externalRef;
    }

    public boolean isSetExternalRef() {
        return ((this.externalRef!= null)&&(!this.externalRef.isEmpty()));
    }

    public void unsetExternalRef() {
        this.externalRef = null;
    }

    /**
     * Gets the value of the errorRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the errorRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getErrorRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getErrorRef() {
        if (errorRef == null) {
            errorRef = new ArrayList<EntityRef>();
        }
        return this.errorRef;
    }

    public boolean isSetErrorRef() {
        return ((this.errorRef!= null)&&(!this.errorRef.isEmpty()));
    }

    public void unsetErrorRef() {
        this.errorRef = null;
    }

    /**
     * Gets the value of the legRestrictions property.
     * 
     * @return
     *     possible object is
     *     {@link LegRestrictions }
     *     
     */
    public LegRestrictions getLegRestrictions() {
        return legRestrictions;
    }

    /**
     * Sets the value of the legRestrictions property.
     * 
     * @param value
     *     allowed object is
     *     {@link LegRestrictions }
     *     
     */
    public void setLegRestrictions(LegRestrictions value) {
        this.legRestrictions = value;
    }

    public boolean isSetLegRestrictions() {
        return (this.legRestrictions!= null);
    }

    /**
     * Gets the value of the line property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the line property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getLine().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Line }
     * 
     * 
     */
    public List<Line> getLine() {
        if (line == null) {
            line = new ArrayList<Line>();
        }
        return this.line;
    }

    public boolean isSetLine() {
        return ((this.line!= null)&&(!this.line.isEmpty()));
    }

    public void unsetLine() {
        this.line = null;
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

    public boolean isSetName() {
        return (this.name!= null);
    }

    /**
     * Gets the value of the status property.
     * 
     * @return
     *     possible object is
     *     {@link ActiveSuspended }
     *     
     */
    public ActiveSuspended getStatus() {
        return status;
    }

    /**
     * Sets the value of the status property.
     * 
     * @param value
     *     allowed object is
     *     {@link ActiveSuspended }
     *     
     */
    public void setStatus(ActiveSuspended value) {
        this.status = value;
    }

    public boolean isSetStatus() {
        return (this.status!= null);
    }

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

    public boolean isSetId() {
        return (this.id!= null);
    }

    /**
     * Gets the value of the documentId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDocumentId() {
        return documentId;
    }

    /**
     * Sets the value of the documentId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDocumentId(String value) {
        this.documentId = value;
    }

    public boolean isSetDocumentId() {
        return (this.documentId!= null);
    }

    /**
     * Gets the value of the provider property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProvider() {
        if (provider == null) {
            return "OpenBet";
        } else {
            return provider;
        }
    }

    /**
     * Sets the value of the provider property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProvider(String value) {
        this.provider = value;
    }

    public boolean isSetProvider() {
        return (this.provider!= null);
    }

    /**
     * Gets the value of the addr property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAddr() {
        return addr;
    }

    /**
     * Sets the value of the addr property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAddr(String value) {
        this.addr = value;
    }

    public boolean isSetAddr() {
        return (this.addr!= null);
    }

    /**
     * Gets the value of the version property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getVersion() {
        return version;
    }

    /**
     * Sets the value of the version property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setVersion(String value) {
        this.version = value;
    }

    public boolean isSetVersion() {
        return (this.version!= null);
    }

    /**
     * Gets the value of the ordering property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getOrdering() {
        return ordering;
    }

    /**
     * Sets the value of the ordering property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setOrdering(BigInteger value) {
        this.ordering = value;
    }

    public boolean isSetOrdering() {
        return (this.ordering!= null);
    }

    /**
     * Gets a map that contains attributes that aren't bound to any typed property on this class.
     * 
     * <p>
     * the map is keyed by the name of the attribute and 
     * the value is the string value of the attribute.
     * 
     * the map returned by this method is live, and you can add new attribute
     * by updating the map directly. Because of this design, there's no setter.
     * 
     * 
     * @return
     *     always non-null
     */
    public Map<QName, String> getOtherAttributes() {
        return otherAttributes;
    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;attribute name="min" use="required" type="{http://schema.openbet.com/core}nonNegativeInt" />
     *       &lt;attribute name="max" use="required" type="{http://schema.openbet.com/core}nonNegativeInt" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "")
    public static class LegRestrictions
        implements Serializable
    {

        private final static long serialVersionUID = 1L;
        @XmlAttribute(required = true)
        protected int min;
        @XmlAttribute(required = true)
        protected int max;
        @XmlAnyAttribute
        private Map<QName, String> otherAttributes = new HashMap<QName, String>();

        /**
         * Gets the value of the min property.
         * 
         */
        public int getMin() {
            return min;
        }

        /**
         * Sets the value of the min property.
         * 
         */
        public void setMin(int value) {
            this.min = value;
        }

        public boolean isSetMin() {
            return true;
        }

        /**
         * Gets the value of the max property.
         * 
         */
        public int getMax() {
            return max;
        }

        /**
         * Sets the value of the max property.
         * 
         */
        public void setMax(int value) {
            this.max = value;
        }

        public boolean isSetMax() {
            return true;
        }

        /**
         * Gets a map that contains attributes that aren't bound to any typed property on this class.
         * 
         * <p>
         * the map is keyed by the name of the attribute and 
         * the value is the string value of the attribute.
         * 
         * the map returned by this method is live, and you can add new attribute
         * by updating the map directly. Because of this design, there's no setter.
         * 
         * 
         * @return
         *     always non-null
         */
        public Map<QName, String> getOtherAttributes() {
            return otherAttributes;
        }

    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;attribute name="combination" use="required" type="{http://schema.products.sportsbook.openbet.com/bet}betLineCombination" />
     *       &lt;attribute name="legs" use="required" type="{http://www.w3.org/2001/XMLSchema}string" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "")
    public static class Line
        implements Serializable
    {

        private final static long serialVersionUID = 1L;
        @XmlAttribute(required = true)
        protected BetLineCombination combination;
        @XmlAttribute(required = true)
        protected String legs;
        @XmlAnyAttribute
        private Map<QName, String> otherAttributes = new HashMap<QName, String>();

        /**
         * Gets the value of the combination property.
         * 
         * @return
         *     possible object is
         *     {@link BetLineCombination }
         *     
         */
        public BetLineCombination getCombination() {
            return combination;
        }

        /**
         * Sets the value of the combination property.
         * 
         * @param value
         *     allowed object is
         *     {@link BetLineCombination }
         *     
         */
        public void setCombination(BetLineCombination value) {
            this.combination = value;
        }

        public boolean isSetCombination() {
            return (this.combination!= null);
        }

        /**
         * Gets the value of the legs property.
         * 
         * @return
         *     possible object is
         *     {@link String }
         *     
         */
        public String getLegs() {
            return legs;
        }

        /**
         * Sets the value of the legs property.
         * 
         * @param value
         *     allowed object is
         *     {@link String }
         *     
         */
        public void setLegs(String value) {
            this.legs = value;
        }

        public boolean isSetLegs() {
            return (this.legs!= null);
        }

        /**
         * Gets a map that contains attributes that aren't bound to any typed property on this class.
         * 
         * <p>
         * the map is keyed by the name of the attribute and 
         * the value is the string value of the attribute.
         * 
         * the map returned by this method is live, and you can add new attribute
         * by updating the map directly. Because of this design, there's no setter.
         * 
         * 
         * @return
         *     always non-null
         */
        public Map<QName, String> getOtherAttributes() {
            return otherAttributes;
        }

    }

}