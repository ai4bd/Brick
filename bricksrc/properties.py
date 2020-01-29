from rdflib import Literal
from .namespaces import A, OWL, RDFS, SKOS, BRICK

"""
Defining properties
"""
properties = {
    # About expectedDomain and expectedRange: They replace temporarily
    # RDFS.domin and RDFS.range. The RDFS.domain and RDFS.range infer
    # the type of the subject and object of a property, respectively.
    # However the type inference can lead to the root class of the types,
    # making all types compatible with each other, thus rendering type
    # contraint using SHACL ineffective.  This problem should be solved
    # by declaring disjointness among certain types but it doesn't seem
    # to work well.
    # Thus, we adopt BRICK.expectedDomain and BRICK.expectedRange which
    # imply nothing about their subject or object, but can be used to
    # validate the type of their subject or object.  See shacl/DESIGN.md
    # for more discussion.
    "expectedDomain": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("Temporary replacement for RDFS.domain"),
    },

    "expectedRange": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("Temporary replacement for RDFS.range"),
    },

    "hasSubproperty": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: RDFS.subPropertyOf,
        BRICK.expectedRange: RDFS.Property,
        BRICK.expectedDomain: RDFS.Property,
        SKOS.definition: Literal("Subject is a property that has the object as its sub-properity")
    },

    "isLocationOf": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "hasLocation",
        BRICK.expectedDomain: BRICK.Location,
        SKOS.definition: Literal("Subject is the physical location encapsulating the object"),
    },
    "hasLocation": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isLocationOf",
        BRICK.expectedRange: BRICK.Location,
        SKOS.definition: Literal("Subject is physically located in the location given by the object"),
    },

    "hasInputSubstance": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        BRICK.expectedRange: BRICK.Substance,
        SKOS.definition: Literal("The subject receives the given substance as an input to its internal process"),
    },
    "hasOutputSubstance": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        BRICK.expectedRange: BRICK.Substance,
        SKOS.definition: Literal("The subject produces or exports the given substance from its internal process"),
    },

    "controls": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isControlledBy",
    },
    "isControlledBy": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "controls",
    },

    "feeds": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("The subject is upstream of the object in the context of some sequential process; some media is passed between them"),
        OWL.inverseOf: "isFedBy",
        # a property may have multiple hasSubproperty predicates
        "hasSubproperty": {
            "feedsAir": {
                SKOS.definition: Literal("Passes air"),
                'substance': BRICK.Air,
                'properties': [BRICK.regulates, BRICK.measures]
            },
        },

        # TODO: add restriction that it needs an air-based equipment on either side?
        # this is equivalent with the classes that have :
        # Restriction (onProperty=brick:hasInputSubstance, hasValue=brick:Air) AND
        # Restriction (onProperty=brick:hasOutputSubstance, hasValue=brick:Air)

        # looks something like this
        #"domain_value_prop": [
        #    [BRICK.hasTag, TAG.Air],
        #],
        #"range_value_prop": [
        #    [BRICK.hasTag, TAG.Air],
        #],
    },
    "isFedBy": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "feeds",
    },

    "hasPoint": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isPointOf",
        SKOS.definition: Literal("The subject has a digital/analog input/output point given by the object"),
        BRICK.expectedRange: BRICK.Point,
    },
    "isPointOf": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "hasPoint",
        BRICK.expectedDomain: BRICK.Point,
    },

    "hasPart": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        SKOS.definition: Literal("The subject is composed in part of the entity given by the object"),
        OWL.inverseOf: "isPartOf",
    },
    "isPartOf": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "hasPart",
    },

    "hasTag": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isTagOf",
        SKOS.definition: Literal("The subject has the given tag"),
        BRICK.expectedRange: BRICK.Tag,
    },
    "isTagOf": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        BRICK.expectedDomain: BRICK.Tag,
    },

    "measures": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isMeasuredBy",
        SKOS.definition: Literal("The subject measures a quantity or substance given by the object"),
        BRICK.expectedDomain: BRICK.Point,
        BRICK.expectedRange: BRICK.Measurable,
    },
    "isMeasuredBy": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        BRICK.expectedDomain: BRICK.Measurable,
        BRICK.expectedRange: BRICK.Point,
    },
    "regulates": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isRegulatedBy",
        SKOS.definition: Literal("The subject contributes to or performs the regulation of the substance given by the object"),
        BRICK.expectedDomain: BRICK.Equipment,
        BRICK.expectedRange: BRICK.Substance,
    },
    "isRegulatedBy": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        BRICK.expectedDomain: BRICK.Substance,
        BRICK.expectedRange: BRICK.Equipment,
    },

    "hasAssociatedTag": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "isAssociatedWith",
        SKOS.definition: Literal("The class is associated with the given tag"),
        RDFS.domain: OWL.Class,
        RDFS.range: BRICK.Tag,
    },
    "isAssociatedWith": {
        A: [OWL.AsymmetricProperty, OWL.IrreflexiveProperty],
        OWL.inverseOf: "hasAssociatedTag",
        SKOS.definition: Literal("The tag is associated with the given class"),
        RDFS.domain: BRICK.Tag,
        RDFS.range: OWL.Class,
    },
}
