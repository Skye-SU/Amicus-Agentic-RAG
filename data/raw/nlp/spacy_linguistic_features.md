Linguistic Features · spaCy Usage Documentation

[# spaCy](/) [💥 **New:** spaCy for PDFs and Word docs](https://github.com/explosion/spacy-layout)

MenuUsageModelsAPIUniverse

* [Usage](/usage)
* [Models](/models)
* [API](/api)
* [Universe](/universe)

Search

# Guides

Select page...Get started › InstallationGet started › Models & LanguagesGet started › Facts & FiguresGet started › spaCy 101Get started › New in v3.7Get started › New in v3.6Get started › New in v3.5Guides › Linguistic FeaturesGuides › Rule-based MatchingGuides › Processing PipelinesGuides › Embeddings & TransformersGuides › Large Language ModelsGuides › Training ModelsGuides › Layers & Model ArchitecturesGuides › spaCy ProjectsGuides › Saving & LoadingGuides › Memory ManagementGuides › VisualizersResources › Project TemplatesResources › v2.x DocumentationResources › Custom Solutions

* Get started
* [Installation](/usage)
* [Models & Languages](/usage/models)
* [Facts & Figures](/usage/facts-figures)
* [spaCy 101](/usage/spacy-101)
* [New in v3.7](/usage/v3-7)
* [New in v3.6](/usage/v3-6)
* [New in v3.5](/usage/v3-5)

* Guides
* [Linguistic Features](/usage/linguistic-features)
  + [POS Tagging](#pos-tagging)
  + [Morphology](#morphology)
  + [Lemmatization](#lemmatization)
  + [Dependency Parse](#dependency-parse)
  + [Named Entities](#named-entities)
  + [Entity Linking](#entity-linking)
  + [Tokenization](#tokenization)
  + [Merging & Splitting](#retokenization)
  + [Sentence Segmentation](#sbd)
  + [Mappings & Exceptions](#mappings-exceptions)
  + [Vectors & Similarity](#vectors-similarity)
  + [Language Data](#language-data)
* [Rule-based Matching](/usage/rule-based-matching)
* [Processing Pipelines](/usage/processing-pipelines)
* [Embeddings & Transformers](/usage/embeddings-transformers)
* [Large Language Models](/usage/large-language-models)
* [Training Models](/usage/training)
* [Layers & Model Architectures](/usage/layers-architectures)
* [spaCy Projects](/usage/projects)
* [Saving & Loading](/usage/saving-loading)
* [Memory Management](/usage/memory-management)
* [Visualizers](/usage/visualizers)

* Resources
* [Project Templates](https://github.com/explosion/projects)
* [v2.x Documentation](https://v2.spacy.io)
* [Custom Solutions](https://explosion.ai/custom-solutions)

# Linguistic Features

Processing raw text intelligently is difficult: most words are rare, and it’s
common for words that look completely different to mean almost the same thing.
The same words in a different order can mean something completely different.
Even splitting text into useful word-like units can be difficult in many
languages. While it’s possible to solve some problems starting from only the raw
characters, it’s usually better to use linguistic knowledge to add useful
information. That’s exactly what spaCy is designed to do: you put in raw text,
and get back a [`Doc`](/api/doc) object, that comes with a variety of
annotations.

## [Part-of-speech tagging](#pos-tagging) Needs model

After tokenization, spaCy can **parse** and **tag** a given `Doc`. This is where
the trained pipeline and its statistical models come in, which enable spaCy to
**make predictions** of which tag or label most likely applies in this context.
A trained component includes binary data that is produced by showing a system
enough examples for it to make predictions that generalize across the language –
for example, a word following “the” in English is most likely a noun.

Linguistic annotations are available as
[`Token` attributes](/api/token#attributes). Like many NLP libraries, spaCy
**encodes all strings to hash values** to reduce memory usage and improve
efficiency. So to get the readable string representation of an attribute, we
need to add an underscore `_` to its name:

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

* **Text:** The original word text.
* **Lemma:** The base form of the word.
* **POS:** The simple [UPOS](https://universaldependencies.org/u/pos/)
  part-of-speech tag.
* **Tag:** The detailed part-of-speech tag.
* **Dep:** Syntactic dependency, i.e. the relation between tokens.
* **Shape:** The word shape – capitalization, punctuation, digits.
* **is alpha:** Is the token an alpha character?
* **is stop:** Is the token part of a stop list, i.e. the most common words of
  the language?

| Text | Lemma | POS | Tag | Dep | Shape | alpha | stop |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apple | apple | `PROPN` | `NNP` | `nsubj` | `Xxxxx` | `True` | `False` |
| is | be | `AUX` | `VBZ` | `aux` | `xx` | `True` | `True` |
| looking | look | `VERB` | `VBG` | `ROOT` | `xxxx` | `True` | `False` |
| at | at | `ADP` | `IN` | `prep` | `xx` | `True` | `True` |
| buying | buy | `VERB` | `VBG` | `pcomp` | `xxxx` | `True` | `False` |
| U.K. | u.k. | `PROPN` | `NNP` | `compound` | `X.X.` | `False` | `False` |
| startup | startup | `NOUN` | `NN` | `dobj` | `xxxx` | `True` | `False` |
| for | for | `ADP` | `IN` | `prep` | `xxx` | `True` | `True` |
| $ | $ | `SYM` | `$` | `quantmod` | `$` | `False` | `False` |
| 1 | 1 | `NUM` | `CD` | `compound` | `d` | `False` | `False` |
| billion | billion | `NUM` | `CD` | `pobj` | `xxxx` | `True` | `False` |

#### Tip: Understanding tags and labels

Most of the tags and labels look pretty abstract, and they vary between
languages. `spacy.explain` will show you a short description – for example,
`spacy.explain("VBZ")` returns “verb, 3rd person singular present”.

Using spaCy’s built-in [displaCy visualizer](/usage/visualizers), here’s what
our example sentence and its dependencies look like:

![](/images/displacy-long.svg)

#### 📖Part-of-speech tag scheme

For a list of the fine-grained and coarse-grained part-of-speech tags assigned
by spaCy’s models across different languages, see the label schemes documented
in the [models directory](/models).

## [Morphology](#morphology)

Inflectional morphology is the process by which a root form of a word is
modified by adding prefixes or suffixes that specify its grammatical function
but do not change its part-of-speech. We say that a **lemma** (root form) is
**inflected** (modified/combined) with one or more **morphological features** to
create a surface form. Here are some examples:

| Context | Surface | Lemma | POS | Morphological Features |
| --- | --- | --- | --- | --- |
| I was reading the paper | reading | read | `VERB` | `VerbForm=Ger` |
| I don’t watch the news, I read the paper | read | read | `VERB` | `VerbForm=Fin`, `Mood=Ind`, `Tense=Pres` |
| I read the paper yesterday | read | read | `VERB` | `VerbForm=Fin`, `Mood=Ind`, `Tense=Past` |

Morphological features are stored in the
[`MorphAnalysis`](/api/morphology#morphanalysis) under `Token.morph`, which
allows you to access individual morphological features.

#### 📝 Things to try

1. Change “I” to “She”. You should see that the morphological features change
   and express that it’s a pronoun in the third person.
2. Inspect `token.morph` for the other tokens.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

### [Statistical morphology](#morphologizer) v3.0Needs model

spaCy’s statistical [`Morphologizer`](/api/morphologizer) component assigns the
morphological features and coarse-grained part-of-speech tags as `Token.morph`
and `Token.pos`.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

### [Rule-based morphology](#rule-based-morphology)

For languages with relatively simple morphological systems like English, spaCy
can assign morphological features through a rule-based approach, which uses the
**token text** and **fine-grained part-of-speech tags** to produce
coarse-grained part-of-speech tags and morphological features.

1. The part-of-speech tagger assigns each token a **fine-grained part-of-speech
   tag**. In the API, these tags are known as `Token.tag`. They express the
   part-of-speech (e.g. verb) and some amount of morphological information, e.g.
   that the verb is past tense (e.g. `VBD` for a past tense verb in the Penn
   Treebank) .
2. For words whose coarse-grained POS is not set by a prior process, a
   [mapping table](/usage/linguistic-features#mappings-exceptions) maps the fine-grained tags to a
   coarse-grained POS tags and morphological features.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

## [Lemmatization](#lemmatization) v3.0

spaCy provides two pipeline components for lemmatization:

1. The [`Lemmatizer`](/api/lemmatizer) component provides lookup and rule-based
   lemmatization methods in a configurable component. An individual language can
   extend the `Lemmatizer` as part of its [language data](/usage/linguistic-features#language-data).
2. The [`EditTreeLemmatizer`](/api/edittreelemmatizer)
   v3.3 component provides a trainable lemmatizer.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

#### Changed in v3.0

Unlike spaCy v2, spaCy v3 models do *not* provide lemmas by default or switch
automatically between lookup and rule-based lemmas depending on whether a tagger
is in the pipeline. To have lemmas in a `Doc`, the pipeline needs to include a
[`Lemmatizer`](/api/lemmatizer) component. The lemmatizer component is
configured to use a single mode such as `"lookup"` or `"rule"` on
initialization. The `"rule"` mode requires `Token.pos` to be set by a previous
component.

The data for spaCy’s lemmatizers is distributed in the package
[`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data). The
provided trained pipelines already include all the required tables, but if you
are creating new pipelines, you’ll probably want to install `spacy-lookups-data`
to provide the data when the lemmatizer is initialized.

### [Lookup lemmatizer](#lemmatizer-lookup)

For pipelines without a tagger or morphologizer, a lookup lemmatizer can be
added to the pipeline as long as a lookup table is provided, typically through
[`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data). The
lookup lemmatizer looks up the token surface form in the lookup table without
reference to the token’s part-of-speech or context.

### [Rule-based lemmatizer](#lemmatizer-rule) Needs model

When training pipelines that include a component that assigns part-of-speech
tags (a morphologizer or a tagger with a [POS mapping](/usage/linguistic-features#mappings-exceptions)), a
rule-based lemmatizer can be added using rule tables from
[`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data):

The rule-based deterministic lemmatizer maps the surface form to a lemma in
light of the previously assigned coarse-grained part-of-speech and morphological
information, without consulting the context of the token. The rule-based
lemmatizer also accepts list-based exception files. For English, these are
acquired from [WordNet](https://wordnet.princeton.edu/).

### [Trainable lemmatizer](#lemmatizer-train) Needs model

The [`EditTreeLemmatizer`](/api/edittreelemmatizer) can learn form-to-lemma
transformations from a training corpus that includes lemma annotations. This
removes the need to write language-specific rules and can (in many cases)
provide higher accuracies than lookup and rule-based lemmatizers.

## [Dependency Parsing](#dependency-parse) Needs model

spaCy features a fast and accurate syntactic dependency parser, and has a rich
API for navigating the tree. The parser also powers the sentence boundary
detection, and lets you iterate over base noun phrases, or “chunks”. You can
check whether a [`Doc`](/api/doc) object has been parsed by calling
`doc.has_annotation("DEP")`, which checks whether the attribute `Token.dep` has
been set returns a boolean value. If the result is `False`, the default sentence
iterator will raise an exception.

#### 📖Dependency label scheme

For a list of the syntactic dependency labels assigned by spaCy’s models across
different languages, see the label schemes documented in the
[models directory](/models).

### [Noun chunks](#noun-chunks)

Noun chunks are “base noun phrases” – flat phrases that have a noun as their
head. You can think of noun chunks as a noun plus the words describing the noun
– for example, “the lavish green grass” or “the world’s largest tech fund”. To
get the noun chunks in a document, simply iterate over
[`Doc.noun_chunks`](/api/doc#noun_chunks).

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

* **Text:** The original noun chunk text.
* **Root text:** The original text of the word connecting the noun chunk to
  the rest of the parse.
* **Root dep:** Dependency relation connecting the root to its head.
* **Root head text:** The text of the root token’s head.

| Text | root.text | root.dep\_ | root.head.text |
| --- | --- | --- | --- |
| Autonomous cars | cars | `nsubj` | shift |
| insurance liability | liability | `dobj` | shift |
| manufacturers | manufacturers | `pobj` | toward |

### [Navigating the parse tree](#navigating)

spaCy uses the terms **head** and **child** to describe the words **connected by
a single arc** in the dependency tree. The term **dep** is used for the arc
label, which describes the type of syntactic relation that connects the child to
the head. As with other attributes, the value of `.dep` is a hash value. You can
get the string value with `.dep_`.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

* **Text:** The original token text.
* **Dep:** The syntactic relation connecting child to head.
* **Head text:** The original text of the token head.
* **Head POS:** The part-of-speech tag of the token head.
* **Children:** The immediate syntactic dependents of the token.

| Text | Dep | Head text | Head POS | Children |
| --- | --- | --- | --- | --- |
| Autonomous | `amod` | cars | `NOUN` |  |
| cars | `nsubj` | shift | `VERB` | Autonomous |
| shift | `ROOT` | shift | `VERB` | cars, liability, toward |
| insurance | `compound` | liability | `NOUN` |  |
| liability | `dobj` | shift | `VERB` | insurance |
| toward | `prep` | shift | `NOUN` | manufacturers |
| manufacturers | `pobj` | toward | `ADP` |  |

![](/images/displacy-long2.svg)

Because the syntactic relations form a tree, every word has **exactly one
head**. You can therefore iterate over the arcs in the tree by iterating over
the words in the sentence. This is usually the best way to match an arc of
interest – from below:

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

If you try to match from above, you’ll have to iterate twice. Once for the head,
and then again through the children:

To iterate through the children, use the `token.children` attribute, which
provides a sequence of [`Token`](/api/token) objects.

#### [Iterating around the local tree](#navigating-around)

A few more convenience attributes are provided for iterating around the local
tree from the token. [`Token.lefts`](/api/token#lefts) and
[`Token.rights`](/api/token#rights) attributes provide sequences of syntactic
children that occur before and after the token. Both sequences are in sentence
order. There are also two integer-typed attributes,
[`Token.n_lefts`](/api/token#n_lefts) and
[`Token.n_rights`](/api/token#n_rights) that give the number of left and right
children.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

You can get a whole phrase by its syntactic head using the
[`Token.subtree`](/api/token#subtree) attribute. This returns an ordered
sequence of tokens. You can walk up the tree with the
[`Token.ancestors`](/api/token#ancestors) attribute, and check dominance with
[`Token.is_ancestor`](/api/token#is_ancestor)

#### Projective vs. non-projective

For the [default English pipelines](/models/en), the parse tree is
**projective**, which means that there are no crossing brackets. The tokens
returned by `.subtree` are therefore guaranteed to be contiguous. This is not
true for the German pipelines, which have many
[non-projective dependencies](https://explosion.ai/blog/german-model#word-order).

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

| Text | Dep | n\_lefts | n\_rights | ancestors |
| --- | --- | --- | --- | --- |
| Credit | `nmod` | `0` | `2` | holders, submit |
| and | `cc` | `0` | `0` | holders, submit |
| mortgage | `compound` | `0` | `0` | account, Credit, holders, submit |
| account | `conj` | `1` | `0` | Credit, holders, submit |
| holders | `nsubj` | `1` | `0` | submit |

Finally, the `.left_edge` and `.right_edge` attributes can be especially useful,
because they give you the first and last token of the subtree. This is the
easiest way to create a `Span` object for a syntactic phrase. Note that
`.right_edge` gives a token **within** the subtree – so if you use it as the
end-point of a range, don’t forget to `+1`!

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

| Text | POS | Dep | Head text |
| --- | --- | --- | --- |
| Credit and mortgage account holders | `NOUN` | `nsubj` | submit |
| must | `VERB` | `aux` | submit |
| submit | `VERB` | `ROOT` | submit |
| their | `ADJ` | `poss` | requests |
| requests | `NOUN` | `dobj` | submit |

The dependency parse can be a useful tool for **information extraction**,
especially when combined with other predictions like
[named entities](/usage/linguistic-features#named-entities). The following example extracts money and
currency values, i.e. entities labeled as `MONEY`, and then uses the dependency
parse to find the noun phrase they are referring to – for example `"Net income"`
→ `"$9.4 million"`.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

#### 📖Combining models and rules

For more examples of how to write rule-based information extraction logic that
takes advantage of the model’s predictions produced by the different components,
see the usage guide on
[combining models and rules](/usage/rule-based-matching#models-rules).

### [Visualizing dependencies](#displacy)

The best way to understand spaCy’s dependency parser is interactively. To make
this easier, spaCy comes with a visualization module. You can pass a `Doc` or a
list of `Doc` objects to displaCy and run
[`displacy.serve`](/api/top-level#displacy.serve) to run the web server, or
[`displacy.render`](/api/top-level#displacy.render) to generate the raw markup.
If you want to know how to write rules that hook into some type of syntactic
construction, just plug the sentence into the visualizer and see how spaCy
annotates it.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

For more details and examples, see the
[usage guide on visualizing spaCy](/usage/visualizers). You can also test
displaCy in our [online demo](https://explosion.ai/demos/displacy)..

### [Disabling the parser](#disabling)

In the [trained pipelines](/models) provided by spaCy, the parser is loaded and
enabled by default as part of the
[standard processing pipeline](/usage/processing-pipelines). If you don’t need
any of the syntactic information, you should disable the parser. Disabling the
parser will make spaCy load and run much faster. If you want to load the parser,
but need to disable it for specific documents, you can also control its use on
the `nlp` object. For more details, see the usage guide on
[disabling pipeline components](/usage/processing-pipelines#disabling).

## [Named Entity Recognition](#named-entities)

spaCy features an extremely fast statistical entity recognition system, that
assigns labels to contiguous spans of tokens. The default
[trained pipelines](/models) can identify a variety of named and numeric
entities, including companies, locations, organizations and products. You can
add arbitrary classes to the entity recognition system, and update the model
with new examples.

### [Named Entity Recognition 101](#named-entities-101)

A named entity is a “real-world object” that’s assigned a name – for example, a
person, a country, a product or a book title. spaCy can **recognize various
types of named entities in a document, by asking the model for a prediction**.
Because models are statistical and strongly depend on the examples they were
trained on, this doesn’t always work *perfectly* and might need some tuning
later, depending on your use case.

Named entities are available as the `ents` property of a `Doc`:

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

* **Text:** The original entity text.
* **Start:** Index of start of entity in the `Doc`.
* **End:** Index of end of entity in the `Doc`.
* **Label:** Entity label, i.e. type.

| Text | Start | End | Label | Description |
| --- | --- | --- | --- | --- |
| Apple | 0 | 5 | `ORG` | Companies, agencies, institutions. |
| U.K. | 27 | 31 | `GPE` | Geopolitical entity, i.e. countries, cities, states. |
| $1 billion | 44 | 54 | `MONEY` | Monetary values, including unit. |

Using spaCy’s built-in [displaCy visualizer](/usage/visualizers), here’s what
our example sentence and its named entities look like:

Apple ORG is looking at buying U.K. GPE startup for $1 billion MONEY

### [Accessing entity annotations and labels](#accessing-ner)

The standard way to access entity annotations is the [`doc.ents`](/api/doc#ents)
property, which produces a sequence of [`Span`](/api/span) objects. The entity
type is accessible either as a hash value or as a string, using the attributes
`ent.label` and `ent.label_`. The `Span` object acts as a sequence of tokens, so
you can iterate over the entity or index into it. You can also get the text form
of the whole entity, as though it were a single token.

You can also access token entity annotations using the
[`token.ent_iob`](/api/token#attributes) and
[`token.ent_type`](/api/token#attributes) attributes. `token.ent_iob` indicates
whether an entity starts, continues or ends on the tag. If no entity type is set
on a token, it will return an empty string.

#### IOB Scheme

* `I` – Token is **inside** an entity.
* `O` – Token is **outside** an entity.
* `B` – Token is the **beginning** of an entity.

#### BILUO Scheme

* `B` – Token is the **beginning** of a multi-token entity.
* `I` – Token is **inside** a multi-token entity.
* `L` – Token is the **last** token of a multi-token entity.
* `U` – Token is a single-token **unit** entity.
* `O` – Token is **outside** an entity.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

| Text | ent\_iob | ent\_iob\_ | ent\_type\_ | Description |
| --- | --- | --- | --- | --- |
| San | `3` | `B` | `"GPE"` | beginning of an entity |
| Francisco | `1` | `I` | `"GPE"` | inside an entity |
| considers | `2` | `O` | `""` | outside an entity |
| banning | `2` | `O` | `""` | outside an entity |
| sidewalk | `2` | `O` | `""` | outside an entity |
| delivery | `2` | `O` | `""` | outside an entity |
| robots | `2` | `O` | `""` | outside an entity |

### [Setting entity annotations](#setting-entities)

To ensure that the sequence of token annotations remains consistent, you have to
set entity annotations **at the document level**. However, you can’t write
directly to the `token.ent_iob` or `token.ent_type` attributes, so the easiest
way to set entities is to use the [`doc.set_ents`](/api/doc#set_ents) function
and create the new entity as a [`Span`](/api/span).

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

Keep in mind that `Span` is initialized with the start and end **token**
indices, not the character offsets. To create a span from character offsets, use
[`Doc.char_span`](/api/doc#char_span):

#### [Setting entity annotations from array](#setting-from-array)

You can also assign entity annotations using the
[`doc.from_array`](/api/doc#from_array) method. To do this, you should include
both the `ENT_TYPE` and the `ENT_IOB` attributes in the array you’re importing
from.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

#### [Setting entity annotations in Cython](#setting-cython)

Finally, you can always write to the underlying struct if you compile a
[Cython](http://cython.org/) function. This is easy to do, and allows you to
write efficient native code.

Obviously, if you write directly to the array of `TokenC*` structs, you’ll have
responsibility for ensuring that the data is left in a consistent state.

### [Built-in entity types](#entity-types)

#### Tip: Understanding entity types

You can also use `spacy.explain()` to get the description for the string
representation of an entity label. For example, `spacy.explain("LANGUAGE")`
will return “any named language”.

#### Annotation scheme

For details on the entity types available in spaCy’s trained pipelines, see the
“label scheme” sections of the individual models in the
[models directory](/models).

### [Visualizing named entities](#displacy)

The
[displaCy ENT visualizer](https://explosion.ai/demos/displacy-ent)
lets you explore an entity recognition model’s behavior interactively. If you’re
training a model, it’s very useful to run the visualization yourself. To help
you do that, spaCy comes with a visualization module. You can pass a `Doc` or a
list of `Doc` objects to displaCy and run
[`displacy.serve`](/api/top-level#displacy.serve) to run the web server, or
[`displacy.render`](/api/top-level#displacy.render) to generate the raw markup.

For more details and examples, see the
[usage guide on visualizing spaCy](/usage/visualizers).

```
#### Named Entity example
```

When Sebastian Thrun PERSON started working on self-driving cars at Google ORG in 2007 DATE, few people outside of the company took him seriously.

## [Entity Linking](#entity-linking)

To ground the named entities into the “real world”, spaCy provides functionality
to perform entity linking, which resolves a textual entity to a unique
identifier from a knowledge base (KB). You can create your own
[`KnowledgeBase`](/api/kb) and [train](/usage/training) a new
[`EntityLinker`](/api/entitylinker) using that custom knowledge base.

As an example on how to define a KnowledgeBase and train an entity linker model,
see [`this tutorial`](https://github.com/explosion/projects/blob/v3/tutorials/nel_emerson)
using [spaCy projects](/usage/projects).

### [Accessing entity identifiers](#entity-linking-accessing) Needs model

The annotated KB identifier is accessible as either a hash value or as a string,
using the attributes `ent.kb_id` and `ent.kb_id_` of a [`Span`](/api/span)
object, or the `ent_kb_id` and `ent_kb_id_` attributes of a
[`Token`](/api/token) object.

## [Tokenization](#tokenization)

Tokenization is the task of splitting a text into meaningful segments, called
*tokens*. The input to the tokenizer is a unicode text, and the output is a
[`Doc`](/api/doc) object. To construct a `Doc` object, you need a
[`Vocab`](/api/vocab) instance, a sequence of `word` strings, and optionally a
sequence of `spaces` booleans, which allow you to maintain alignment of the
tokens into the original string.

#### Important note

spaCy’s tokenization is **non-destructive**, which means that you’ll always be
able to reconstruct the original input from the tokenized output. Whitespace
information is preserved in the tokens and no information is added or removed
during tokenization. This is kind of a core principle of spaCy’s `Doc` object:
`doc.text == input_text` should always hold true.

During processing, spaCy first **tokenizes** the text, i.e. segments it into
words, punctuation and so on. This is done by applying rules specific to each
language. For example, punctuation at the end of a sentence should be split off
– whereas “U.K.” should remain one token. Each `Doc` consists of individual
tokens, and we can iterate over them:

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Apple | is | looking | at | buying | U.K. | startup | for | $ | 1 | billion |

First, the raw text is split on whitespace characters, similar to
`text.split(' ')`. Then, the tokenizer processes the text from left to right. On
each substring, it performs two checks:

1. **Does the substring match a tokenizer exception rule?** For example, “don’t”
   does not contain whitespace, but should be split into two tokens, “do” and
   “n’t”, while “U.K.” should always remain one token.
2. **Can a prefix, suffix or infix be split off?** For example punctuation like
   commas, periods, hyphens or quotes.

If there’s a match, the rule is applied and the tokenizer continues its loop,
starting with the newly split substrings. This way, spaCy can split **complex,
nested tokens** like combinations of abbreviations and multiple punctuation
marks.

* **Tokenizer exception:** Special-case rule to split a string into several
  tokens or prevent a token from being split when punctuation rules are
  applied.
* **Prefix:** Character(s) at the beginning, e.g. `$`, `(`, `“`, `¿`.
* **Suffix:** Character(s) at the end, e.g. `km`, `)`, `”`, `!`.
* **Infix:** Character(s) in between, e.g. `-`, `--`, `/`, `…`.

![Example of the tokenization process](/images/tokenization.svg)

While punctuation rules are usually pretty general, tokenizer exceptions
strongly depend on the specifics of the individual language. This is why each
[available language](/usage/models#languages) has its own subclass, like
`English` or `German`, that loads in lists of hard-coded data and exception
rules.

#### Algorithm details: How spaCy's tokenizer works[¶](/usage/linguistic-features#how-tokenizer-works)

spaCy introduces a novel tokenization algorithm that gives a better balance
between performance, ease of definition and ease of alignment into the original
string.

After consuming a prefix or suffix, we consult the special cases again. We want
the special cases to handle things like “don’t” in English, and we want the same
rule to work for “(don’t)!“. We do this by splitting off the open bracket, then
the exclamation, then the closed bracket, and finally matching the special case.
Here’s an implementation of the algorithm in Python optimized for readability
rather than performance:

The algorithm can be summarized as follows:

1. Iterate over space-separated substrings.
2. Check whether we have an explicitly defined special case for this substring.
   If we do, use it.
3. Look for a token match. If there is a match, stop processing and keep this
   token.
4. Check whether we have an explicitly defined special case for this substring.
   If we do, use it.
5. Otherwise, try to consume one prefix. If we consumed a prefix, go back to #3,
   so that the token match and special cases always get priority.
6. If we didn’t consume a prefix, try to consume a suffix and then go back to
   #3.
7. If we can’t consume a prefix or a suffix, look for a URL match.
8. If there’s no URL match, then look for a special case.
9. Look for “infixes” – stuff like hyphens etc. and split the substring into
   tokens on all infixes.
10. Once we can’t consume any more of the string, handle it as a single token.
11. Make a final pass over the text to check for special cases that include
    spaces or that were missed due to the incremental processing of affixes.

**Global** and **language-specific** tokenizer data is supplied via the language
data in [`spacy/lang`](https://github.com/explosion/spaCy/tree/master/spacy/lang). The tokenizer exceptions
define special cases like “don’t” in English, which needs to be split into two
tokens: `{ORTH: "do"}` and `{ORTH: "n't", NORM: "not"}`. The prefixes, suffixes
and infixes mostly define punctuation rules – for example, when to split off
periods (at the end of a sentence), and when to leave tokens containing periods
intact (abbreviations like “U.S.”).

#### Should I change the language data or add custom tokenizer rules?[¶](/usage/linguistic-features#lang-data-vs-tokenizer)

Tokenization rules that are specific to one language, but can be **generalized
across that language**, should ideally live in the language data in
[`spacy/lang`](https://github.com/explosion/spaCy/tree/master/spacy/lang) – we always appreciate pull requests!
Anything that’s specific to a domain or text type – like financial trading
abbreviations or Bavarian youth slang – should be added as a special case rule
to your tokenizer instance. If you’re dealing with a lot of customizations, it
might make sense to create an entirely custom subclass.

---

### [Adding special case tokenization rules](#special-cases)

Most domains have at least some idiosyncrasies that require custom tokenization
rules. This could be very certain expressions, or abbreviations only used in
this specific field. Here’s how to add a special case rule to an existing
[`Tokenizer`](/api/tokenizer) instance:

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

The special case doesn’t have to match an entire whitespace-delimited substring.
The tokenizer will incrementally split off punctuation, and keep looking up the
remaining substring. The special case rules also have precedence over the
punctuation splitting.

#### [Debugging the tokenizer](#tokenizer-debug)

A working implementation of the pseudo-code above is available for debugging as
[`nlp.tokenizer.explain(text)`](/api/tokenizer#explain). It returns a list of
tuples showing which tokenizer rule or pattern was matched for each token. The
tokens produced are identical to `nlp.tokenizer()` except for whitespace tokens:

#### Expected output

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

### [Customizing spaCy’s Tokenizer class](#native-tokenizers)

Let’s imagine you wanted to create a tokenizer for a new language or specific
domain. There are six things you may need to define:

1. A dictionary of **special cases**. This handles things like contractions,
   units of measurement, emoticons, certain abbreviations, etc.
2. A function `prefix_search`, to handle **preceding punctuation**, such as open
   quotes, open brackets, etc.
3. A function `suffix_search`, to handle **succeeding punctuation**, such as
   commas, periods, close quotes, etc.
4. A function `infix_finditer`, to handle non-whitespace separators, such as
   hyphens etc.
5. An optional boolean function `token_match` matching strings that should never
   be split, overriding the infix rules. Useful for things like numbers.
6. An optional boolean function `url_match`, which is similar to `token_match`
   except that prefixes and suffixes are removed before applying the match.

You shouldn’t usually need to create a `Tokenizer` subclass. Standard usage is
to use `re.compile()` to build a regular expression object, and pass its
`.search()` and `.finditer()` methods:

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

If you need to subclass the tokenizer instead, the relevant methods to
specialize are `find_prefix`, `find_suffix` and `find_infix`.

#### Important note

When customizing the prefix, suffix and infix handling, remember that you’re
passing in **functions** for spaCy to execute, e.g. `prefix_re.search` – not
just the regular expressions. This means that your functions also need to define
how the rules should be applied. For example, if you’re adding your own prefix
rules, you need to make sure they’re only applied to characters at the
**beginning of a token**, e.g. by adding `^`. Similarly, suffix rules should
only be applied at the **end of a token**, so your expression should end with a
`$`.

#### [Modifying existing rule sets](#native-tokenizer-additions)

In many situations, you don’t necessarily need entirely custom rules. Sometimes
you just want to add another character to the prefixes, suffixes or infixes. The
default prefix, suffix and infix rules are available via the `nlp` object’s
`Defaults` and the `Tokenizer` attributes such as
[`Tokenizer.suffix_search`](/api/tokenizer#attributes) are writable, so you can
overwrite them with compiled regular expression objects using modified default
rules. spaCy ships with utility functions to help you compile the regular
expressions – for example,
[`compile_suffix_regex`](/api/top-level#util.compile_suffix_regex):

Similarly, you can remove a character from the default suffixes:

The `Tokenizer.suffix_search` attribute should be a function which takes a
unicode string and returns a **regex match object** or `None`. Usually we use
the `.search` attribute of a compiled regex object, but you can use some other
function that behaves the same way.

#### Important note

If you’ve loaded a trained pipeline, writing to the
[`nlp.Defaults`](/api/language#defaults) or `English.Defaults` directly won’t
work, since the regular expressions are read from the pipeline data and will be
compiled when you load it. If you modify `nlp.Defaults`, you’ll only see the
effect if you call [`spacy.blank`](/api/top-level#spacy.blank). If you want to
modify the tokenizer loaded from a trained pipeline, you should modify
`nlp.tokenizer` directly. If you’re training your own pipeline, you can register
[callbacks](/usage/training#custom-code-nlp-callbacks) to modify the `nlp`
object before training.

The prefix, infix and suffix rule sets include not only individual characters
but also detailed regular expressions that take the surrounding context into
account. For example, there is a regular expression that treats a hyphen between
letters as an infix. If you do not want the tokenizer to split on hyphens
between letters, you can modify the existing infix definition from
[`lang/punctuation.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py):

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

For an overview of the default regular expressions, see
[`lang/punctuation.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py) and
language-specific definitions such as
[`lang/de/punctuation.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/de/punctuation.py) for
German.

### [Hooking a custom tokenizer into the pipeline](#custom-tokenizer)

The tokenizer is the first component of the processing pipeline and the only one
that can’t be replaced by writing to `nlp.pipeline`. This is because it has a
different signature from all the other components: it takes a text and returns a
[`Doc`](/api/doc), whereas all other components expect to already receive a
tokenized `Doc`.

![The processing pipeline](/images/pipeline.svg)

To overwrite the existing tokenizer, you need to replace `nlp.tokenizer` with a
custom function that takes a text and returns a [`Doc`](/api/doc).

#### Creating a Doc

Constructing a [`Doc`](/api/doc) object manually requires at least two
arguments: the shared `Vocab` and a list of words. Optionally, you can pass in
a list of `spaces` values indicating whether the token at this position is
followed by a space (default `True`). See the section on
[pre-tokenized text](/usage/linguistic-features#own-annotations) for more info.

| Argument | Type | Description |
| --- | --- | --- |
| `text` | `str` | The raw text to tokenize. |
| **RETURNS** | [`Doc`](/api/doc) | The tokenized document. |

#### [Example 1: Basic whitespace tokenizer](#custom-tokenizer-example)

Here’s an example of the most basic whitespace tokenizer. It takes the shared
vocab, so it can construct `Doc` objects. When it’s called on a text, it returns
a `Doc` object consisting of the text split on single space characters. We can
then overwrite the `nlp.tokenizer` attribute with an instance of our custom
tokenizer.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

#### [Example 2: Third-party tokenizers (BERT word pieces)](#custom-tokenizer-example2)

You can use the same approach to plug in any other third-party tokenizers. Your
custom callable just needs to return a `Doc` object with the tokens produced by
your tokenizer. In this example, the wrapper uses the **BERT word piece
tokenizer**, provided by the
[`tokenizers`](https://github.com/huggingface/tokenizers) library. The tokens
available in the `Doc` object returned by spaCy now match the exact word pieces
produced by the tokenizer.

#### 💡 Tip: spacy-transformers

If you’re working with transformer models like BERT, check out the
[`spacy-transformers`](https://github.com/explosion/spacy-transformers)
extension package and [documentation](/usage/embeddings-transformers). It
includes a pipeline component for using pretrained transformer weights and
**training transformer models** in spaCy, as well as helpful utilities for
aligning word pieces to linguistic tokenization.

```
#### Custom BERT word piece tokenizer
```

#### Important note on tokenization and models

Keep in mind that your models’ results may be less accurate if the tokenization
during training differs from the tokenization at runtime. So if you modify a
trained pipeline’s tokenization afterwards, it may produce very different
predictions. You should therefore train your pipeline with the **same
tokenizer** it will be using at runtime. See the docs on
[training with custom tokenization](/usage/linguistic-features#custom-tokenizer-training) for details.

#### [Training with custom tokenization](#custom-tokenizer-training) v3.0

spaCy’s [training config](/usage/training#config) describes the settings,
hyperparameters, pipeline and tokenizer used for constructing and training the
pipeline. The `[nlp.tokenizer]` block refers to a **registered function** that
takes the `nlp` object and returns a tokenizer. Here, we’re registering a
function called `whitespace_tokenizer` in the
[`@tokenizers` registry](/api/top-level#registry). To make sure spaCy knows how
to construct your tokenizer during training, you can pass in your Python file by
setting `--code functions.py` when you run [`spacy train`](/api/cli#train).

#### config.cfg

```
#### functions.py
```

Registered functions can also take arguments that are then passed in from the
config. This allows you to quickly change and keep track of different settings.
Here, the registered function called `bert_word_piece_tokenizer` takes two
arguments: the path to a vocabulary file and whether to lowercase the text. The
Python type hints `str` and `bool` ensure that the received values have the
correct type.

#### config.cfg

```
#### functions.py
```

To avoid hard-coding local paths into your config file, you can also set the
vocab path on the CLI by using the `--nlp.tokenizer.vocab_file`
[override](/usage/training#config-overrides) when you run
[`spacy train`](/api/cli#train). For more details on using registered functions,
see the docs in [training with custom code](/usage/training#custom-code).

Remember that a registered function should always be a function that spaCy
**calls to create something**, not the “something” itself. In this case, it
**creates a function** that takes the `nlp` object and returns a callable that
takes a text and returns a `Doc`.

#### [Using pre-tokenized text](#own-annotations)

spaCy generally assumes by default that your data is **raw text**. However,
sometimes your data is partially annotated, e.g. with pre-existing tokenization,
part-of-speech tags, etc. The most common situation is that you have
**pre-defined tokenization**. If you have a list of strings, you can create a
[`Doc`](/api/doc) object directly. Optionally, you can also specify a list of
boolean values, indicating whether each word is followed by a space.

#### ✏️ Things to try

1. Change a boolean value in the list of `spaces`. You should see it reflected
   in the `doc.text` and whether the token is followed by a space.
2. Remove `spaces=spaces` from the `Doc`. You should see that every token is
   now followed by a space.
3. Copy-paste a random sentence from the internet and manually construct a
   `Doc` with `words` and `spaces` so that the `doc.text` matches the original
   input text.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

If provided, the spaces list must be the **same length** as the words list. The
spaces list affects the `doc.text`, `span.text`, `token.idx`, `span.start_char`
and `span.end_char` attributes. If you don’t provide a `spaces` sequence, spaCy
will assume that all words are followed by a space. Once you have a
[`Doc`](/api/doc) object, you can write to its attributes to set the
part-of-speech tags, syntactic dependencies, named entities and other
attributes.

#### [Aligning tokenization](#aligning-tokenization)

spaCy’s tokenization is non-destructive and uses language-specific rules
optimized for compatibility with treebank annotations. Other tools and resources
can sometimes tokenize things differently – for example, `"I'm"` →
`["I", "'", "m"]` instead of `["I", "'m"]`.

In situations like that, you often want to align the tokenization so that you
can merge annotations from different sources together, or take vectors predicted
by a
[pretrained BERT model](https://github.com/huggingface/pytorch-transformers) and
apply them to spaCy tokens. spaCy’s [`Alignment`](/api/example#alignment-object)
object allows the one-to-one mappings of token indices in both directions as
well as taking into account indices where multiple tokens align to one single
token.

#### ✏️ Things to try

1. Change the capitalization in one of the token lists – for example,
   `"obama"` to `"Obama"`. You’ll see that the alignment is case-insensitive.
2. Change `"podcasts"` in `other_tokens` to `"pod", "casts"`. You should see
   that there are now two tokens of length 2 in `y2x`, one corresponding to
   “‘s”, and one to “podcasts”.
3. Make `other_tokens` and `spacy_tokens` identical. You’ll see that all
   tokens now correspond 1-to-1.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

Here are some insights from the alignment information generated in the example
above:

* The one-to-one mappings for the first four tokens are identical, which means
  they map to each other. This makes sense because they’re also identical in the
  input: `"i"`, `"listened"`, `"to"` and `"obama"`.
* The value of `x2y.data[6]` is `5`, which means that `other_tokens[6]`
  (`"podcasts"`) aligns to `spacy_tokens[5]` (also `"podcasts"`).
* `x2y.data[4]` and `x2y.data[5]` are both `4`, which means that both tokens 4
  and 5 of `other_tokens` (`"'"` and `"s"`) align to token 4 of `spacy_tokens`
  (`"'s"`).

#### Important note

The current implementation of the alignment algorithm assumes that both
tokenizations add up to the same string. For example, you’ll be able to align
`["I", "'", "m"]` and `["I", "'m"]`, which both add up to `"I'm"`, but not
`["I", "'m"]` and `["I", "am"]`.

## [Merging and splitting](#retokenization)

The [`Doc.retokenize`](/api/doc#retokenize) context manager lets you merge and
split tokens. Modifications to the tokenization are stored and performed all at
once when the context manager exits. To merge several tokens into one single
token, pass a `Span` to [`retokenizer.merge`](/api/doc#retokenizer.merge). An
optional dictionary of `attrs` lets you set attributes that will be assigned to
the merged token – for example, the lemma, part-of-speech tag or entity type. By
default, the merged token will receive the same attributes as the merged span’s
root.

#### ✏️ Things to try

1. Inspect the `token.lemma_` attribute with and without setting the `attrs`.
   You’ll see that the lemma defaults to “New”, the lemma of the span’s root.
2. Overwrite other attributes like the `"ENT_TYPE"`. Since “New York” is also
   recognized as a named entity, this change will also be reflected in the
   `doc.ents`.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

#### Tip: merging entities and noun phrases

If you need to merge named entities or noun chunks, check out the built-in
[`merge_entities`](/api/pipeline-functions#merge_entities) and
[`merge_noun_chunks`](/api/pipeline-functions#merge_noun_chunks) pipeline
components. When added to your pipeline using `nlp.add_pipe`, they’ll take
care of merging the spans automatically.

If an attribute in the `attrs` is a context-dependent token attribute, it will
be applied to the underlying [`Token`](/api/token). For example `LEMMA`, `POS`
or `DEP` only apply to a word in context, so they’re token attributes. If an
attribute is a context-independent lexical attribute, it will be applied to the
underlying [`Lexeme`](/api/lexeme), the entry in the vocabulary. For example,
`LOWER` or `IS_STOP` apply to all words of the same spelling, regardless of the
context.

#### Note on merging overlapping spans

If you’re trying to merge spans that overlap, spaCy will raise an error because
it’s unclear how the result should look. Depending on the application, you may
want to match the shortest or longest possible span, so it’s up to you to filter
them. If you’re looking for the longest non-overlapping span, you can use the
[`util.filter_spans`](/api/top-level#util.filter_spans) helper:

### Splitting tokens

The [`retokenizer.split`](/api/doc#retokenizer.split) method allows splitting
one token into two or more tokens. This can be useful for cases where
tokenization rules alone aren’t sufficient. For example, you might want to split
“its” into the tokens “it” and “is” – but not the possessive pronoun “its”. You
can write rule-based logic that can find only the correct “its” to split, but by
that time, the `Doc` will already be tokenized.

This process of splitting a token requires more settings, because you need to
specify the text of the individual tokens, optional per-token attributes and how
the tokens should be attached to the existing syntax tree. This can be done by
supplying a list of `heads` – either the token to attach the newly split token
to, or a `(token, subtoken)` tuple if the newly split token should be attached
to another subtoken. In this case, “New” should be attached to “York” (the
second split subtoken) and “York” should be attached to “in”.

#### ✏️ Things to try

1. Assign different attributes to the subtokens and compare the result.
2. Change the heads so that “New” is attached to “in” and “York” is attached
   to “New”.
3. Split the token into three tokens instead of two – for example,
   `["New", "Yo", "rk"]`.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

Specifying the heads as a list of `token` or `(token, subtoken)` tuples allows
attaching split subtokens to other subtokens, without having to keep track of
the token indices after splitting.

| Token | Head | Description |
| --- | --- | --- |
| `"New"` | `(doc[3], 1)` | Attach this token to the second subtoken (index `1`) that `doc[3]` will be split into, i.e. “York”. |
| `"York"` | `doc[2]` | Attach this token to `doc[1]` in the original `Doc`, i.e. “in”. |

If you don’t care about the heads (for example, if you’re only running the
tokenizer and not the parser), you can attach each subtoken to itself:

#### Important note

When splitting tokens, the subtoken texts always have to match the original
token text – or, put differently `"".join(subtokens) == token.text` always needs
to hold true. If this wasn’t the case, splitting tokens could easily end up
producing confusing and unexpected results that would contradict spaCy’s
non-destructive tokenization policy.

### [Overwriting custom extension attributes](#retokenization-extensions)

If you’ve registered custom
[extension attributes](/usage/processing-pipelines#custom-components-attributes),
you can overwrite them during tokenization by providing a dictionary of
attribute names mapped to new values as the `"_"` key in the `attrs`. For
merging, you need to provide one dictionary of attributes for the resulting
merged token. For splitting, you need to provide a list of dictionaries with
custom attributes, one per split subtoken.

#### Important note

To set extension attributes during retokenization, the attributes need to be
**registered** using the [`Token.set_extension`](/api/token#set_extension)
method and they need to be **writable**. This means that they should either have
a default value that can be overwritten, or a getter *and* setter. Method
extensions or extensions with only a getter are computed dynamically, so their
values can’t be overwritten. For more details, see the
[extension attribute docs](/usage/processing-pipelines#custom-components-attributes).

#### ✏️ Things to try

1. Add another custom extension – maybe `"music_style"`? – and overwrite it.
2. Change the extension attribute to use only a `getter` function. You should
   see that spaCy raises an error, because the attribute is not writable
   anymore.
3. Rewrite the code to split a token with `retokenizer.split`. Remember that
   you need to provide a list of extension attribute values as the `"_"`
   property, one for each split subtoken.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

## [Sentence Segmentation](#sbd)

A [`Doc`](/api/doc) object’s sentences are available via the `Doc.sents`
property. To view a `Doc`’s sentences, you can iterate over the `Doc.sents`, a
generator that yields [`Span`](/api/span) objects. You can check whether a `Doc`
has sentence boundaries by calling
[`Doc.has_annotation`](/api/doc#has_annotation) with the attribute name
`"SENT_START"`.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

spaCy provides four alternatives for sentence segmentation:

1. [Dependency parser](/usage/linguistic-features#sbd-parser): the statistical
   [`DependencyParser`](/api/dependencyparser) provides the most accurate
   sentence boundaries based on full dependency parses.
2. [Statistical sentence segmenter](/usage/linguistic-features#sbd-senter): the statistical
   [`SentenceRecognizer`](/api/sentencerecognizer) is a simpler and faster
   alternative to the parser that only sets sentence boundaries.
3. [Rule-based pipeline component](/usage/linguistic-features#sbd-component): the rule-based
   [`Sentencizer`](/api/sentencizer) sets sentence boundaries using a
   customizable list of sentence-final punctuation.
4. [Custom function](/usage/linguistic-features#sbd-custom): your own custom function added to the
   processing pipeline can set sentence boundaries by writing to
   `Token.is_sent_start`.

### [Default: Using the dependency parse](#sbd-parser) Needs model

Unlike other libraries, spaCy uses the dependency parse to determine sentence
boundaries. This is usually the most accurate approach, but it requires a
**trained pipeline** that provides accurate predictions. If your texts are
closer to general-purpose news or web text, this should work well out-of-the-box
with spaCy’s provided trained pipelines. For social media or conversational text
that doesn’t follow the same rules, your application may benefit from a custom
trained or rule-based component.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

spaCy’s dependency parser respects already set boundaries, so you can preprocess
your `Doc` using custom components *before* it’s parsed. Depending on your text,
this may also improve parse accuracy, since the parser is constrained to predict
parses consistent with the sentence boundaries.

### [Statistical sentence segmenter](#sbd-senter) v3.0Needs model

The [`SentenceRecognizer`](/api/sentencerecognizer) is a simple statistical
component that only provides sentence boundaries. Along with being faster and
smaller than the parser, its primary advantage is that it’s easier to train
because it only requires annotated sentence boundaries rather than full
dependency parses. spaCy’s [trained pipelines](/models) include both a parser
and a trained sentence segmenter, which is
[disabled](/usage/processing-pipelines#disabling) by default. If you only need
sentence boundaries and no parser, you can use the `exclude` or `disable`
argument on [`spacy.load`](/api/top-level#spacy.load) to load the pipeline
without the parser and then enable the sentence recognizer explicitly with
[`nlp.enable_pipe`](/api/language#enable_pipe).

#### senter vs. parser

The recall for the `senter` is typically slightly lower than for the parser,
which is better at predicting sentence boundaries when punctuation is not
present.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

### [Rule-based pipeline component](#sbd-component)

The [`Sentencizer`](/api/sentencizer) component is a
[pipeline component](/usage/processing-pipelines) that splits sentences on
punctuation like `.`, `!` or `?`. You can plug it into your pipeline if you only
need sentence boundaries without dependency parses.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

### [Custom rule-based strategy](#sbd-custom)

If you want to implement your own strategy that differs from the default
rule-based approach of splitting on sentences, you can also create a
[custom pipeline component](/usage/processing-pipelines#custom-components) that
takes a `Doc` object and sets the `Token.is_sent_start` attribute on each
individual token. If set to `False`, the token is explicitly marked as *not* the
start of a sentence. If set to `None` (default), it’s treated as a missing value
and can still be overwritten by the parser.

#### Important note

To prevent inconsistent state, you can only set boundaries **before** a document
is parsed (and `doc.has_annotation("DEP")` is `False`). To ensure that your
component is added in the right place, you can set `before='parser'` or
`first=True` when adding it to the pipeline using
[`nlp.add_pipe`](/api/language#add_pipe).

Here’s an example of a component that implements a pre-processing rule for
splitting on `"..."` tokens. The component is added before the parser, which is
then used to further segment the text. That’s possible, because `is_sent_start`
is only set to `True` for some of the tokens – all others still specify `None`
for unset sentence boundaries. This approach can be useful if you want to
implement **additional** rules specific to your data, while still being able to
take advantage of dependency-based sentence segmentation.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

## [Mappings & Exceptions](#mappings-exceptions) v3.0

The [`AttributeRuler`](/api/attributeruler) manages **rule-based mappings and
exceptions** for all token-level attributes. As the number of
[pipeline components](/api#architecture-pipeline) has grown from spaCy v2 to
v3, handling rules and exceptions in each component individually has become
impractical, so the `AttributeRuler` provides a single component with a unified
pattern format for all token attribute mappings and exceptions.

The `AttributeRuler` uses
[`Matcher` patterns](/usage/rule-based-matching#adding-patterns) to identify
tokens and then assigns them the provided attributes. If needed, the
[`Matcher`](/api/matcher) patterns can include context around the target token.
For example, the attribute ruler can:

* provide exceptions for any **token attributes**
* map **fine-grained tags** to **coarse-grained tags** for languages without
  statistical morphologizers (replacing the v2.x `tag_map` in the
  [language data](/usage/linguistic-features#language-data))
* map token **surface form + fine-grained tags** to **morphological features**
  (replacing the v2.x `morph_rules` in the [language data](/usage/linguistic-features#language-data))
* specify the **tags for space tokens** (replacing hard-coded behavior in the
  tagger)

The following example shows how the tag and POS `NNP`/`PROPN` can be specified
for the phrase `"The Who"`, overriding the tags provided by the statistical
tagger and the POS tag map.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

#### Migrating from spaCy v2.x

The [`AttributeRuler`](/api/attributeruler) can import a **tag map and morph
rules** in the v2.x format via its built-in methods or when the component is
initialized before training. See the
[migration guide](/usage/v3#migrating-training-mappings-exceptions) for details.

## [Word vectors and semantic similarity](#vectors-similarity)

Similarity is determined by comparing **word vectors** or “word embeddings”,
multi-dimensional meaning representations of a word. Word vectors can be
generated using an algorithm like
[word2vec](https://en.wikipedia.org/wiki/Word2vec) and usually look like this:

```
#### banana.vector
```

#### Important note

To make them compact and fast, spaCy’s small [pipeline packages](/models) (all
packages that end in `sm`) **don’t ship with word vectors**, and only include
context-sensitive **tensors**. This means you can still use the `similarity()`
methods to compare documents, spans and tokens – but the result won’t be as
good, and individual tokens won’t have any vectors assigned. So in order to use
*real* word vectors, you need to download a larger pipeline package:

Pipeline packages that come with built-in word vectors make them available as
the [`Token.vector`](/api/token#vector) attribute.
[`Doc.vector`](/api/doc#vector) and [`Span.vector`](/api/span#vector) will
default to an average of their token vectors. You can also check if a token has
a vector assigned, and get the L2 norm, which can be used to normalize vectors.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

* **Text**: The original token text.
* **has vector**: Does the token have a vector representation?
* **Vector norm**: The L2 norm of the token’s vector (the square root of the
  sum of the values squared)
* **OOV**: Out-of-vocabulary

The words “dog”, “cat” and “banana” are all pretty common in English, so they’re
part of the pipeline’s vocabulary, and come with a vector. The word “afskfsd” on
the other hand is a lot less common and out-of-vocabulary – so its vector
representation consists of 300 dimensions of `0`, which means it’s practically
nonexistent. If your application will benefit from a **large vocabulary** with
more vectors, you should consider using one of the larger pipeline packages or
loading in a full vector package, for example,
[`en_core_web_lg`](/models/en#en_core_web_lg), which includes **685k unique
vectors**.

spaCy is able to compare two objects, and make a prediction of **how similar
they are**. Predicting similarity is useful for building recommendation systems
or flagging duplicates. For example, you can suggest a user content that’s
similar to what they’re currently looking at, or label a support ticket as a
duplicate if it’s very similar to an already existing one.

Each [`Doc`](/api/doc), [`Span`](/api/span), [`Token`](/api/token) and
[`Lexeme`](/api/lexeme) comes with a [`.similarity`](/api/token#similarity)
method that lets you compare it with another object, and determine the
similarity. Of course similarity is always subjective – whether two words, spans
or documents are similar really depends on how you’re looking at it. spaCy’s
similarity implementation usually assumes a pretty general-purpose definition of
similarity.

#### 📝 Things to try

1. Compare two different tokens and try to find the two most *dissimilar*
   tokens in the texts with the lowest similarity score (according to the
   vectors).
2. Compare the similarity of two [`Lexeme`](/api/lexeme) objects, entries in
   the vocabulary. You can get a lexeme via the `.lex` attribute of a token.
   You should see that the similarity results are identical to the token
   similarity.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

### [What to expect from similarity results](#similarity-expectations)

Computing similarity scores can be helpful in many situations, but it’s also
important to maintain **realistic expectations** about what information it can
provide. Words can be related to each other in many ways, so a single
“similarity” score will always be a **mix of different signals**, and vectors
trained on different data can produce very different results that may not be
useful for your purpose. Here are some important considerations to keep in mind:

* There’s no objective definition of similarity. Whether “I like burgers” and “I
  like pasta” is similar **depends on your application**. Both talk about food
  preferences, which makes them very similar – but if you’re analyzing mentions
  of food, those sentences are pretty dissimilar, because they talk about very
  different foods.
* The similarity of [`Doc`](/api/doc) and [`Span`](/api/span) objects defaults
  to the **average** of the token vectors. This means that the vector for “fast
  food” is the average of the vectors for “fast” and “food”, which isn’t
  necessarily representative of the phrase “fast food”.
* Vector averaging means that the vector of multiple tokens is **insensitive to
  the order** of the words. Two documents expressing the same meaning with
  dissimilar wording will return a lower similarity score than two documents
  that happen to contain the same words while expressing different meanings.

#### 💡Tip: Check out sense2vec

[![sense2vec Screenshot](/images/sense2vec.jpg)](https://github.com/explosion/sense2vec)

[`sense2vec`](https://github.com/explosion/sense2vec) is a library developed by
us that builds on top of spaCy and lets you train and query more interesting and
detailed word vectors. It combines noun phrases like “fast food” or “fair game”
and includes the part-of-speech tags and entity labels. The library also
includes annotation recipes for our annotation tool [Prodigy](https://prodi.gy)
that let you evaluate vectors and create terminology lists. For more details,
check out [our blog post](https://explosion.ai/blog/sense2vec-reloaded). To
explore the semantic similarities across all Reddit comments of 2015 and 2019,
see the [interactive demo](https://explosion.ai/demos/sense2vec).

### [Adding word vectors](#adding-vectors)

Custom word vectors can be trained using a number of open-source libraries, such
as [Gensim](https://radimrehurek.com/gensim), [FastText](https://fasttext.cc),
or Tomas Mikolov’s original
[Word2vec implementation](https://code.google.com/archive/p/word2vec/). Most
word vector libraries output an easy-to-read text-based format, where each line
consists of the word followed by its vector. For everyday use, we want to
convert the vectors into a binary format that loads faster and takes up less
space on disk. The easiest way to do this is the
[`init vectors`](/api/cli#init-vectors) command-line utility. This will output a
blank spaCy pipeline in the directory `/tmp/la_vectors_wiki_lg`, giving you
access to some nice Latin vectors. You can then pass the directory path to
[`spacy.load`](/api/top-level#spacy.load) or use it in the
[`[initialize]`](/api/data-formats#config-initialize) of your config when you
[train](/usage/training) a model.

#### Usage example

#### How to optimize vector coverage[¶](/usage/linguistic-features#custom-vectors-coverage)

To help you strike a good balance between coverage and memory usage, spaCy’s
[`Vectors`](/api/vectors) class lets you map **multiple keys** to the **same
row** of the table. If you’re using the
[`spacy init vectors`](/api/cli#init-vectors) command to create a vocabulary,
pruning the vectors will be taken care of automatically if you set the `--prune`
flag. You can also do it manually in the following steps:

1. Start with a **word vectors package** that covers a huge vocabulary. For
   instance, the [`en_core_web_lg`](/models/en#en_core_web_lg) package provides
   300-dimensional GloVe vectors for 685k terms of English.
2. If your vocabulary has values set for the `Lexeme.prob` attribute, the
   lexemes will be sorted by descending probability to determine which vectors
   to prune. Otherwise, lexemes will be sorted by their order in the `Vocab`.
3. Call [`Vocab.prune_vectors`](/api/vocab#prune_vectors) with the number of
   vectors you want to keep.

[`Vocab.prune_vectors`](/api/vocab#prune_vectors) reduces the current vector
table to a given number of unique entries, and returns a dictionary containing
the removed words, mapped to `(string, score)` tuples, where `string` is the
entry the removed word was mapped to and `score` the similarity score between
the two words.

```
#### Removed words
```

In the example above, the vector for “Shore” was removed and remapped to the
vector of “coast”, which is deemed about 73% similar. “Leaving” was remapped to
the vector of “leaving”, which is identical. If you’re using the
[`init vectors`](/api/cli#init-vectors) command, you can set the `--prune`
option to easily reduce the size of the vectors as you add them to a spaCy
pipeline:

This will create a blank spaCy pipeline with vectors for the first 10,000 words
in the vectors. All other words in the vectors are mapped to the closest vector
among those retained.

### [Adding vectors individually](#adding-individual-vectors)

The `vector` attribute is a **read-only** numpy or cupy array (depending on
whether you’ve configured spaCy to use GPU memory), with dtype `float32`. The
array is read-only so that spaCy can avoid unnecessary copy operations where
possible. You can modify the vectors via the [`Vocab`](/api/vocab) or
[`Vectors`](/api/vectors) table. Using the
[`Vocab.set_vector`](/api/vocab#set_vector) method is often the easiest approach
if you have vectors in an arbitrary format, as you can read in the vectors with
your own logic, and just set them with a simple loop. This method is likely to
be slower than approaches that work with the whole vectors table at once, but
it’s a great approach for once-off conversions before you save out your `nlp`
object to disk.

```
#### Adding vectors
```

## [Language Data](#language-data)

Every language is different – and usually full of **exceptions and special
cases**, especially amongst the most common words. Some of these exceptions are
shared across languages, while others are **entirely specific** – usually so
specific that they need to be hard-coded. The
[`lang`](https://github.com/explosion/spaCy/tree/master/spacy/lang) module contains all language-specific data,
organized in simple Python files. This makes the data easy to update and extend.

The **shared language data** in the directory root includes rules that can be
generalized across languages – for example, rules for basic punctuation, emoji,
emoticons and single-letter abbreviations. The **individual language data** in a
submodule contains rules that are only relevant to a particular language. It
also takes care of putting together all components and creating the
[`Language`](/api/language) subclass – for example, `English` or `German`. The
values are defined in the [`Language.Defaults`](/api/language#defaults).

| Name | Description |
| --- | --- |
| **Stop words** [`stop_words.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/en/stop_words.py) | List of most common words of a language that are often useful to filter out, for example “and” or “I”. Matching tokens will return `True` for `is_stop`. |
| **Tokenizer exceptions** [`tokenizer_exceptions.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/de/tokenizer_exceptions.py) | Special-case rules for the tokenizer, for example, contractions like “can’t” and abbreviations with punctuation, like “U.K.”. |
| **Punctuation rules** [`punctuation.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py) | Regular expressions for splitting tokens, e.g. on punctuation or special characters like emoji. Includes rules for prefixes, suffixes and infixes. |
| **Character classes** [`char_classes.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/char_classes.py) | Character classes to be used in regular expressions, for example, Latin characters, quotes, hyphens or icons. |
| **Lexical attributes** [`lex_attrs.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/en/lex_attrs.py) | Custom functions for setting lexical attributes on tokens, e.g. `like_num`, which includes language-specific words like “ten” or “hundred”. |
| **Syntax iterators** [`syntax_iterators.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/en/syntax_iterators.py) | Functions that compute views of a `Doc` object based on its syntax. At the moment, only used for [noun chunks](/usage/linguistic-features#noun-chunks). |
| **Lemmatizer** [`lemmatizer.py`](https://github.com/explosion/spaCy/tree/master/spacy/lang/fr/lemmatizer.py) [`spacy-lookups-data`](https://github.com/explosion/spacy-lookups-data) | Custom lemmatizer implementation and lemmatization tables. |

### [Creating a custom language subclass](#language-subclass)

If you want to customize multiple components of the language data or add support
for a custom language or domain-specific “dialect”, you can also implement your
own language subclass. The subclass should define two attributes: the `lang`
(unique language code) and the `Defaults` defining the language data. For an
overview of the available attributes that can be overwritten, see the
[`Language.Defaults`](/api/language#defaults) documentation.

```
#### Editable CodespaCy v3.7 · Python 3 · via Binder



run
```

The [`@spacy.registry.languages`](/api/top-level#registry) decorator lets you
register a custom language class and assign it a string name. This means that
you can call [`spacy.blank`](/api/top-level#spacy.blank) with your custom
language name, and even train pipelines with it and refer to it in your
[training config](/usage/training#config).

#### Config usage

After registering your custom language class using the `languages` registry,
you can refer to it in your [training config](/usage/training#config). This
means spaCy will train your pipeline using the custom subclass.

In order to resolve `"custom_en"` to your subclass, the registered function
needs to be available during training. You can load a Python file containing
the code using the `--code` argument:

```
#### Registering a custom language
```

[Suggest edits](https://github.com/explosion/spaCy/tree/master/website/docs/usage/linguistic-features.mdx)

[Read nextRule-based Matching](/usage/rule-based-matching)

* spaCy
* [Usage](/usage)
* [Models](/models)
* [API Reference](/api)
* [Online Course](https://course.spacy.io)
* [Custom Solutions](https://explosion.ai/custom-solutions)

* Community
* [Universe](/universe)
* [GitHub Discussions](https://github.com/explosion/spaCy/discussions)
* [Issue Tracker](https://github.com/explosion/spaCy/issues)
* [Stack Overflow](http://stackoverflow.com/questions/tagged/spacy)
* [Merchandise](https://explosion.ai/merch)

* Connect
* [Bluesky](https://bsky.app/profile/explosion-ai.bsky.social)
* [GitHub](https://github.com/explosion/spaCy)
* [Live Stream](https://www.youtube.com/playlist?list=PLBmcuObd5An5_iAxNYLJa_xWmNzsYce8c)
* [YouTube](https://youtube.com/c/ExplosionAI)
* [Blog](https://explosion.ai/blog)

* Stay in the loop!
* Receive updates about new releases, tutorials and more.
* Sign up

© 2016-2025 [Explosion](https://explosion.ai)[Legal / Imprint](https://explosion.ai/legal)

{"props":{"pageProps":{"title":"Linguistic Features","next":{"slug":"/usage/rule-based-matching","title":"Rule-based Matching"},"menu":[["POS Tagging","pos-tagging"],["Morphology","morphology"],["Lemmatization","lemmatization"],["Dependency Parse","dependency-parse"],["Named Entities","named-entities"],["Entity Linking","entity-linking"],["Tokenization","tokenization"],["Merging \u0026 Splitting","retokenization"],["Sentence Segmentation","sbd"],["Mappings \u0026 Exceptions","mappings-exceptions"],["Vectors \u0026 Similarity","vectors-similarity"],["Language Data","language-data"]],"slug":"/usage/linguistic-features","mdx":{"compiledSource":"/\*@jsxRuntime automatic @jsxImportSource react\*/\nconst {Fragment: \_Fragment, jsx: \_jsx, jsxs: \_jsxs} = arguments[0];\nconst {useMDXComponents: \_provideComponents} = arguments[0];\nfunction \_createMdxContent(props) {\n const \_components = Object.assign({\n section: \"section\",\n p: \"p\",\n a: \"a\",\n h2: \"h2\",\n strong: \"strong\",\n table: \"table\",\n thead: \"thead\",\n tr: \"tr\",\n th: \"th\",\n tbody: \"tbody\",\n td: \"td\",\n blockquote: \"blockquote\",\n h4: \"h4\",\n ol: \"ol\",\n li: \"li\",\n pre: \"pre\",\n code: \"code\",\n h3: \"h3\",\n em: \"em\",\n ul: \"ul\",\n hr: \"hr\",\n img: \"img\"\n }, \_provideComponents(), props.components), {InlineCode, PosDeps101, Infobox, Tag, ImageScrollable, NER101, Standalone, Tokenization101, Accordion, Vectors101, LanguageData101} = \_components;\n if (!Accordion) \_missingMdxReference(\"Accordion\", true);\n if (!ImageScrollable) \_missingMdxReference(\"ImageScrollable\", true);\n if (!Infobox) \_missingMdxReference(\"Infobox\", true);\n if (!InlineCode) \_missingMdxReference(\"InlineCode\", true);\n if (!LanguageData101) \_missingMdxReference(\"LanguageData101\", true);\n if (!NER101) \_missingMdxReference(\"NER101\", true);\n if (!PosDeps101) \_missingMdxReference(\"PosDeps101\", true);\n if (!Standalone) \_missingMdxReference(\"Standalone\", true);\n if (!Tag) \_missingMdxReference(\"Tag\", true);\n if (!Tokenization101) \_missingMdxReference(\"Tokenization101\", true);\n if (!Vectors101) \_missingMdxReference(\"Vectors101\", true);\n return \_jsxs(\_Fragment, {\n children: [\_jsx(\_components.section, {\n children: \_jsxs(\_components.p, {\n children: [\"Processing raw text intelligently is difficult: most words are rare, and it’s\\ncommon for words that look completely different to mean almost the same thing.\\nThe same words in a different order can mean something completely different.\\nEven splitting text into useful word-like units can be difficult in many\\nlanguages. While it’s possible to solve some problems starting from only the raw\\ncharacters, it’s usually better to use linguistic knowledge to add useful\\ninformation. That’s exactly what spaCy is designed to do: you put in raw text,\\nand get back a \", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object, that comes with a variety of\\nannotations.\"]\n })\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-pos-tagging\",\n children: [\_jsx(\_components.h2, {\n id: \"pos-tagging\",\n model: \"tagger, parser\",\n children: \"Part-of-speech tagging \"\n }), \_jsx(PosDeps101, {}), \_jsx(Infobox, {\n title: \"Part-of-speech tag scheme\",\n emoji: \"📖\",\n children: \_jsxs(\_components.p, {\n children: [\"For a list of the fine-grained and coarse-grained part-of-speech tags assigned\\nby spaCy’s models across different languages, see the label schemes documented\\nin the \", \_jsx(\_components.a, {\n href: \"/models\",\n children: \"models directory\"\n }), \".\"]\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-morphology\",\n children: [\_jsx(\_components.h2, {\n id: \"morphology\",\n children: \"Morphology \"\n }), \_jsxs(\_components.p, {\n children: [\"Inflectional morphology is the process by which a root form of a word is\\nmodified by adding prefixes or suffixes that specify its grammatical function\\nbut do not change its part-of-speech. We say that a \", \_jsx(\_components.strong, {\n children: \"lemma\"\n }), \" (root form) is\\n\", \_jsx(\_components.strong, {\n children: \"inflected\"\n }), \" (modified/combined) with one or more \", \_jsx(\_components.strong, {\n children: \"morphological features\"\n }), \" to\\ncreate a surface form. Here are some examples:\"]\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Context\"\n }), \_jsx(\_components.th, {\n children: \"Surface\"\n }), \_jsx(\_components.th, {\n children: \"Lemma\"\n }), \_jsx(\_components.th, {\n children: \"POS\"\n }), \_jsx(\_components.th, {\n children: \"Morphological Features\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"I was reading the paper\"\n }), \_jsx(\_components.td, {\n children: \"reading\"\n }), \_jsx(\_components.td, {\n children: \"read\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VerbForm=Ger\"\n })\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"I don’t watch the news, I read the paper\"\n }), \_jsx(\_components.td, {\n children: \"read\"\n }), \_jsx(\_components.td, {\n children: \"read\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsxs(\_components.td, {\n children: [\_jsx(InlineCode, {\n children: \"VerbForm=Fin\"\n }), \", \", \_jsx(InlineCode, {\n children: \"Mood=Ind\"\n }), \", \", \_jsx(InlineCode, {\n children: \"Tense=Pres\"\n })]\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"I read the paper yesterday\"\n }), \_jsx(\_components.td, {\n children: \"read\"\n }), \_jsx(\_components.td, {\n children: \"read\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsxs(\_components.td, {\n children: [\_jsx(InlineCode, {\n children: \"VerbForm=Fin\"\n }), \", \", \_jsx(InlineCode, {\n children: \"Mood=Ind\"\n }), \", \", \_jsx(InlineCode, {\n children: \"Tense=Past\"\n })]\n })]\n })]\n })]\n }), \_jsxs(\_components.p, {\n children: [\"Morphological features are stored in the\\n\", \_jsx(\_components.a, {\n href: \"/api/morphology#morphanalysis\",\n children: \_jsx(InlineCode, {\n children: \"MorphAnalysis\"\n })\n }), \" under \", \_jsx(InlineCode, {\n children: \"Token.morph\"\n }), \", which\\nallows you to access individual morphological features.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"📝 Things to try\"\n }), \"\\n\", \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsx(\_components.li, {\n children: \"Change “I” to “She”. You should see that the morphological features change\\nand express that it’s a pronoun in the third person.\"\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Inspect \", \_jsx(InlineCode, {\n children: \"token.morph\"\n }), \" for the other tokens.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\nprint(\\\"Pipeline:\\\", nlp.pipe\_names)\\ndoc = nlp(\\\"I was reading the paper.\\\")\\ntoken = doc[0] # 'I'\\nprint(token.morph) # 'Case=Nom|Number=Sing|Person=1|PronType=Prs'\\nprint(token.morph.get(\\\"PronType\\\")) # ['Prs']\\n\"\n })\n }), \_jsx(\_components.h3, {\n id: \"morphologizer\",\n version: \"3\",\n model: \"morphologizer\",\n children: \"Statistical morphology \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy’s statistical \", \_jsx(\_components.a, {\n href: \"/api/morphologizer\",\n children: \_jsx(InlineCode, {\n children: \"Morphologizer\"\n })\n }), \" component assigns the\\nmorphological features and coarse-grained part-of-speech tags as \", \_jsx(InlineCode, {\n children: \"Token.morph\"\n }), \"\\nand \", \_jsx(InlineCode, {\n children: \"Token.pos\"\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"de\_core\_news\_sm\\\")\\ndoc = nlp(\\\"Wo bist du?\\\") # English: 'Where are you?'\\nprint(doc[2].morph) # 'Case=Nom|Number=Sing|Person=2|PronType=Prs'\\nprint(doc[2].pos\_) # 'PRON'\\n\"\n })\n }), \_jsx(\_components.h3, {\n id: \"rule-based-morphology\",\n children: \"Rule-based morphology \"\n }), \_jsxs(\_components.p, {\n children: [\"For languages with relatively simple morphological systems like English, spaCy\\ncan assign morphological features through a rule-based approach, which uses the\\n\", \_jsx(\_components.strong, {\n children: \"token text\"\n }), \" and \", \_jsx(\_components.strong, {\n children: \"fine-grained part-of-speech tags\"\n }), \" to produce\\ncoarse-grained part-of-speech tags and morphological features.\"]\n }), \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"The part-of-speech tagger assigns each token a \", \_jsx(\_components.strong, {\n children: \"fine-grained part-of-speech\\ntag\"\n }), \". In the API, these tags are known as \", \_jsx(InlineCode, {\n children: \"Token.tag\"\n }), \". They express the\\npart-of-speech (e.g. verb) and some amount of morphological information, e.g.\\nthat the verb is past tense (e.g. \", \_jsx(InlineCode, {\n children: \"VBD\"\n }), \" for a past tense verb in the Penn\\nTreebank) .\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"For words whose coarse-grained POS is not set by a prior process, a\\n\", \_jsx(\_components.a, {\n href: \"#mappings-exceptions\",\n children: \"mapping table\"\n }), \" maps the fine-grained tags to a\\ncoarse-grained POS tags and morphological features.\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Where are you?\\\")\\nprint(doc[2].morph) # 'Case=Nom|Person=2|PronType=Prs'\\nprint(doc[2].pos\_) # 'PRON'\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-lemmatization\",\n children: [\_jsx(\_components.h2, {\n id: \"lemmatization\",\n version: \"3\",\n children: \"Lemmatization \"\n }), \_jsx(\_components.p, {\n children: \"spaCy provides two pipeline components for lemmatization:\"\n }), \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/lemmatizer\",\n children: \_jsx(InlineCode, {\n children: \"Lemmatizer\"\n })\n }), \" component provides lookup and rule-based\\nlemmatization methods in a configurable component. An individual language can\\nextend the \", \_jsx(InlineCode, {\n children: \"Lemmatizer\"\n }), \" as part of its \", \_jsx(\_components.a, {\n href: \"#language-data\",\n children: \"language data\"\n }), \".\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/edittreelemmatizer\",\n children: \_jsx(InlineCode, {\n children: \"EditTreeLemmatizer\"\n })\n }), \"\\n\", \_jsx(Tag, {\n variant: \"new\",\n children: \"3.3\"\n }), \" component provides a trainable lemmatizer.\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\n# English pipelines include a rule-based lemmatizer\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\nlemmatizer = nlp.get\_pipe(\\\"lemmatizer\\\")\\nprint(lemmatizer.mode) # 'rule'\\n\\ndoc = nlp(\\\"I was reading the paper.\\\")\\nprint([token.lemma\_ for token in doc])\\n# ['I', 'be', 'read', 'the', 'paper', '.']\\n\"\n })\n }), \_jsx(Infobox, {\n title: \"Changed in v3.0\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"Unlike spaCy v2, spaCy v3 models do \", \_jsx(\_components.em, {\n children: \"not\"\n }), \" provide lemmas by default or switch\\nautomatically between lookup and rule-based lemmas depending on whether a tagger\\nis in the pipeline. To have lemmas in a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \", the pipeline needs to include a\\n\", \_jsx(\_components.a, {\n href: \"/api/lemmatizer\",\n children: \_jsx(InlineCode, {\n children: \"Lemmatizer\"\n })\n }), \" component. The lemmatizer component is\\nconfigured to use a single mode such as \", \_jsx(InlineCode, {\n children: \"\\\"lookup\\\"\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"\\\"rule\\\"\"\n }), \" on\\ninitialization. The \", \_jsx(InlineCode, {\n children: \"\\\"rule\\\"\"\n }), \" mode requires \", \_jsx(InlineCode, {\n children: \"Token.pos\"\n }), \" to be set by a previous\\ncomponent.\"]\n })\n }), \_jsxs(\_components.p, {\n children: [\"The data for spaCy’s lemmatizers is distributed in the package\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spacy-lookups-data\",\n children: \_jsx(InlineCode, {\n children: \"spacy-lookups-data\"\n })\n }), \". The\\nprovided trained pipelines already include all the required tables, but if you\\nare creating new pipelines, you’ll probably want to install \", \_jsx(InlineCode, {\n children: \"spacy-lookups-data\"\n }), \"\\nto provide the data when the lemmatizer is initialized.\"]\n }), \_jsx(\_components.h3, {\n id: \"lemmatizer-lookup\",\n children: \"Lookup lemmatizer \"\n }), \_jsxs(\_components.p, {\n children: [\"For pipelines without a tagger or morphologizer, a lookup lemmatizer can be\\nadded to the pipeline as long as a lookup table is provided, typically through\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spacy-lookups-data\",\n children: \_jsx(InlineCode, {\n children: \"spacy-lookups-data\"\n })\n }), \". The\\nlookup lemmatizer looks up the token surface form in the lookup table without\\nreference to the token’s part-of-speech or context.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"# pip install -U spacy[lookups]\\nimport spacy\\n\\nnlp = spacy.blank(\\\"sv\\\")\\nnlp.add\_pipe(\\\"lemmatizer\\\", config={\\\"mode\\\": \\\"lookup\\\"})\\n\"\n })\n }), \_jsx(\_components.h3, {\n id: \"lemmatizer-rule\",\n model: \"morphologizer\",\n children: \"Rule-based lemmatizer \"\n }), \_jsxs(\_components.p, {\n children: [\"When training pipelines that include a component that assigns part-of-speech\\ntags (a morphologizer or a tagger with a \", \_jsx(\_components.a, {\n href: \"#mappings-exceptions\",\n children: \"POS mapping\"\n }), \"), a\\nrule-based lemmatizer can be added using rule tables from\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spacy-lookups-data\",\n children: \_jsx(InlineCode, {\n children: \"spacy-lookups-data\"\n })\n }), \":\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"# pip install -U spacy[lookups]\\nimport spacy\\n\\nnlp = spacy.blank(\\\"de\\\")\\n# Morphologizer (note: model is not yet trained!)\\nnlp.add\_pipe(\\\"morphologizer\\\")\\n# Rule-based lemmatizer\\nnlp.add\_pipe(\\\"lemmatizer\\\", config={\\\"mode\\\": \\\"rule\\\"})\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"The rule-based deterministic lemmatizer maps the surface form to a lemma in\\nlight of the previously assigned coarse-grained part-of-speech and morphological\\ninformation, without consulting the context of the token. The rule-based\\nlemmatizer also accepts list-based exception files. For English, these are\\nacquired from \", \_jsx(\_components.a, {\n href: \"https://wordnet.princeton.edu/\",\n children: \"WordNet\"\n }), \".\"]\n }), \_jsx(\_components.h3, {\n id: \"lemmatizer-train\",\n model: \"trainable\_lemmatizer\",\n children: \"Trainable lemmatizer \"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/edittreelemmatizer\",\n children: \_jsx(InlineCode, {\n children: \"EditTreeLemmatizer\"\n })\n }), \" can learn form-to-lemma\\ntransformations from a training corpus that includes lemma annotations. This\\nremoves the need to write language-specific rules and can (in many cases)\\nprovide higher accuracies than lookup and rule-based lemmatizers.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"import spacy\\n\\nnlp = spacy.blank(\\\"de\\\")\\nnlp.add\_pipe(\\\"trainable\_lemmatizer\\\", name=\\\"lemmatizer\\\")\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-dependency-parse\",\n children: [\_jsx(\_components.h2, {\n id: \"dependency-parse\",\n model: \"parser\",\n children: \"Dependency Parsing \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy features a fast and accurate syntactic dependency parser, and has a rich\\nAPI for navigating the tree. The parser also powers the sentence boundary\\ndetection, and lets you iterate over base noun phrases, or “chunks”. You can\\ncheck whether a \", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object has been parsed by calling\\n\", \_jsx(InlineCode, {\n children: \"doc.has\_annotation(\\\"DEP\\\")\"\n }), \", which checks whether the attribute \", \_jsx(InlineCode, {\n children: \"Token.dep\"\n }), \" has\\nbeen set returns a boolean value. If the result is \", \_jsx(InlineCode, {\n children: \"False\"\n }), \", the default sentence\\niterator will raise an exception.\"]\n }), \_jsx(Infobox, {\n title: \"Dependency label scheme\",\n emoji: \"📖\",\n children: \_jsxs(\_components.p, {\n children: [\"For a list of the syntactic dependency labels assigned by spaCy’s models across\\ndifferent languages, see the label schemes documented in the\\n\", \_jsx(\_components.a, {\n href: \"/models\",\n children: \"models directory\"\n }), \".\"]\n })\n }), \_jsx(\_components.h3, {\n id: \"noun-chunks\",\n children: \"Noun chunks \"\n }), \_jsxs(\_components.p, {\n children: [\"Noun chunks are “base noun phrases” – flat phrases that have a noun as their\\nhead. You can think of noun chunks as a noun plus the words describing the noun\\n– for example, “the lavish green grass” or “the world’s largest tech fund”. To\\nget the noun chunks in a document, simply iterate over\\n\", \_jsx(\_components.a, {\n href: \"/api/doc#noun\_chunks\",\n children: \_jsx(InlineCode, {\n children: \"Doc.noun\_chunks\"\n })\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Autonomous cars shift insurance liability toward manufacturers\\\")\\nfor chunk in doc.noun\_chunks:\\n print(chunk.text, chunk.root.text, chunk.root.dep\_,\\n chunk.root.head.text)\\n\"\n })\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsxs(\_components.ul, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Text:\"\n }), \" The original noun chunk text.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Root text:\"\n }), \" The original text of the word connecting the noun chunk to\\nthe rest of the parse.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Root dep:\"\n }), \" Dependency relation connecting the root to its head.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Root head text:\"\n }), \" The text of the root token’s head.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Text\"\n }), \_jsx(\_components.th, {\n children: \"root.text\"\n }), \_jsx(\_components.th, {\n children: \"root.dep\_\"\n }), \_jsx(\_components.th, {\n children: \"root.head.text\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"Autonomous cars\"\n }), \_jsx(\_components.td, {\n children: \"cars\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"nsubj\"\n })\n }), \_jsx(\_components.td, {\n children: \"shift\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"insurance liability\"\n }), \_jsx(\_components.td, {\n children: \"liability\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"dobj\"\n })\n }), \_jsx(\_components.td, {\n children: \"shift\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"manufacturers\"\n }), \_jsx(\_components.td, {\n children: \"manufacturers\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"pobj\"\n })\n }), \_jsx(\_components.td, {\n children: \"toward\"\n })]\n })]\n })]\n }), \_jsx(\_components.h3, {\n id: \"navigating\",\n children: \"Navigating the parse tree \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy uses the terms \", \_jsx(\_components.strong, {\n children: \"head\"\n }), \" and \", \_jsx(\_components.strong, {\n children: \"child\"\n }), \" to describe the words \", \_jsx(\_components.strong, {\n children: \"connected by\\na single arc\"\n }), \" in the dependency tree. The term \", \_jsx(\_components.strong, {\n children: \"dep\"\n }), \" is used for the arc\\nlabel, which describes the type of syntactic relation that connects the child to\\nthe head. As with other attributes, the value of \", \_jsx(InlineCode, {\n children: \".dep\"\n }), \" is a hash value. You can\\nget the string value with \", \_jsx(InlineCode, {\n children: \".dep\_\"\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Autonomous cars shift insurance liability toward manufacturers\\\")\\nfor token in doc:\\n print(token.text, token.dep\_, token.head.text, token.head.pos\_,\\n [child for child in token.children])\\n\"\n })\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsxs(\_components.ul, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Text:\"\n }), \" The original token text.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Dep:\"\n }), \" The syntactic relation connecting child to head.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Head text:\"\n }), \" The original text of the token head.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Head POS:\"\n }), \" The part-of-speech tag of the token head.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.strong, {\n children: \"Children:\"\n }), \" The immediate syntactic dependents of the token.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Text\"\n }), \_jsx(\_components.th, {\n children: \"Dep\"\n }), \_jsx(\_components.th, {\n children: \"Head text\"\n }), \_jsx(\_components.th, {\n children: \"Head POS\"\n }), \_jsx(\_components.th, {\n children: \"Children\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"Autonomous\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"amod\"\n })\n }), \_jsx(\_components.td, {\n children: \"cars\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"NOUN\"\n })\n }), \_jsx(\_components.td, {})]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"cars\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"nsubj\"\n })\n }), \_jsx(\_components.td, {\n children: \"shift\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsx(\_components.td, {\n children: \"Autonomous\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"shift\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"ROOT\"\n })\n }), \_jsx(\_components.td, {\n children: \"shift\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsx(\_components.td, {\n children: \"cars, liability, toward\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"insurance\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"compound\"\n })\n }), \_jsx(\_components.td, {\n children: \"liability\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"NOUN\"\n })\n }), \_jsx(\_components.td, {})]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"liability\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"dobj\"\n })\n }), \_jsx(\_components.td, {\n children: \"shift\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsx(\_components.td, {\n children: \"insurance\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"toward\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"prep\"\n })\n }), \_jsx(\_components.td, {\n children: \"shift\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"NOUN\"\n })\n }), \_jsx(\_components.td, {\n children: \"manufacturers\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"manufacturers\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"pobj\"\n })\n }), \_jsx(\_components.td, {\n children: \"toward\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"ADP\"\n })\n }), \_jsx(\_components.td, {})]\n })]\n })]\n }), \_jsx(ImageScrollable, {\n src: \"/images/displacy-long2.svg\",\n width: 1275\n }), \_jsxs(\_components.p, {\n children: [\"Because the syntactic relations form a tree, every word has \", \_jsx(\_components.strong, {\n children: \"exactly one\\nhead\"\n }), \". You can therefore iterate over the arcs in the tree by iterating over\\nthe words in the sentence. This is usually the best way to match an arc of\\ninterest – from below:\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.symbols import nsubj, VERB\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Autonomous cars shift insurance liability toward manufacturers\\\")\\n\\n# Finding a verb with a subject from below — good\\nverbs = set()\\nfor possible\_subject in doc:\\n if possible\_subject.dep == nsubj and possible\_subject.head.pos == VERB:\\n verbs.add(possible\_subject.head)\\nprint(verbs)\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"If you try to match from above, you’ll have to iterate twice. Once for the head,\\nand then again through the children:\"\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"# Finding a verb with a subject from above — less good\\nverbs = []\\nfor possible\_verb in doc:\\n if possible\_verb.pos == VERB:\\n for possible\_subject in possible\_verb.children:\\n if possible\_subject.dep == nsubj:\\n verbs.append(possible\_verb)\\n break\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"To iterate through the children, use the \", \_jsx(InlineCode, {\n children: \"token.children\"\n }), \" attribute, which\\nprovides a sequence of \", \_jsx(\_components.a, {\n href: \"/api/token\",\n children: \_jsx(InlineCode, {\n children: \"Token\"\n })\n }), \" objects.\"]\n }), \_jsx(\_components.h4, {\n id: \"navigating-around\",\n children: \"Iterating around the local tree \"\n }), \_jsxs(\_components.p, {\n children: [\"A few more convenience attributes are provided for iterating around the local\\ntree from the token. \", \_jsx(\_components.a, {\n href: \"/api/token#lefts\",\n children: \_jsx(InlineCode, {\n children: \"Token.lefts\"\n })\n }), \" and\\n\", \_jsx(\_components.a, {\n href: \"/api/token#rights\",\n children: \_jsx(InlineCode, {\n children: \"Token.rights\"\n })\n }), \" attributes provide sequences of syntactic\\nchildren that occur before and after the token. Both sequences are in sentence\\norder. There are also two integer-typed attributes,\\n\", \_jsx(\_components.a, {\n href: \"/api/token#n\_lefts\",\n children: \_jsx(InlineCode, {\n children: \"Token.n\_lefts\"\n })\n }), \" and\\n\", \_jsx(\_components.a, {\n href: \"/api/token#n\_rights\",\n children: \_jsx(InlineCode, {\n children: \"Token.n\_rights\"\n })\n }), \" that give the number of left and right\\nchildren.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"bright red apples on the tree\\\")\\nprint([token.text for token in doc[2].lefts]) # ['bright', 'red']\\nprint([token.text for token in doc[2].rights]) # ['on']\\nprint(doc[2].n\_lefts) # 2\\nprint(doc[2].n\_rights) # 1\\n\"\n })\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"de\_core\_news\_sm\\\")\\ndoc = nlp(\\\"schöne rote Äpfel auf dem Baum\\\")\\nprint([token.text for token in doc[2].lefts]) # ['schöne', 'rote']\\nprint([token.text for token in doc[2].rights]) # ['auf']\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"You can get a whole phrase by its syntactic head using the\\n\", \_jsx(\_components.a, {\n href: \"/api/token#subtree\",\n children: \_jsx(InlineCode, {\n children: \"Token.subtree\"\n })\n }), \" attribute. This returns an ordered\\nsequence of tokens. You can walk up the tree with the\\n\", \_jsx(\_components.a, {\n href: \"/api/token#ancestors\",\n children: \_jsx(InlineCode, {\n children: \"Token.ancestors\"\n })\n }), \" attribute, and check dominance with\\n\", \_jsx(\_components.a, {\n href: \"/api/token#is\_ancestor\",\n children: \_jsx(InlineCode, {\n children: \"Token.is\_ancestor\"\n })\n })]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Projective vs. non-projective\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"For the \", \_jsx(\_components.a, {\n href: \"/models/en\",\n children: \"default English pipelines\"\n }), \", the parse tree is\\n\", \_jsx(\_components.strong, {\n children: \"projective\"\n }), \", which means that there are no crossing brackets. The tokens\\nreturned by \", \_jsx(InlineCode, {\n children: \".subtree\"\n }), \" are therefore guaranteed to be contiguous. This is not\\ntrue for the German pipelines, which have many\\n\", \_jsx(\_components.a, {\n href: \"https://explosion.ai/blog/german-model#word-order\",\n children: \"non-projective dependencies\"\n }), \".\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Credit and mortgage account holders must submit their requests\\\")\\n\\nroot = [token for token in doc if token.head == token][0]\\nsubject = list(root.lefts)[0]\\nfor descendant in subject.subtree:\\n assert subject is descendant or subject.is\_ancestor(descendant)\\n print(descendant.text, descendant.dep\_, descendant.n\_lefts,\\n descendant.n\_rights,\\n [ancestor.text for ancestor in descendant.ancestors])\\n\"\n })\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Text\"\n }), \_jsx(\_components.th, {\n children: \"Dep\"\n }), \_jsx(\_components.th, {\n children: \"n\_lefts\"\n }), \_jsx(\_components.th, {\n children: \"n\_rights\"\n }), \_jsx(\_components.th, {\n children: \"ancestors\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"Credit\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"nmod\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"2\"\n })\n }), \_jsx(\_components.td, {\n children: \"holders, submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"and\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"cc\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \"holders, submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"mortgage\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"compound\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \"account, Credit, holders, submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"account\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"conj\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"1\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \"Credit, holders, submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"holders\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"nsubj\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"1\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"0\"\n })\n }), \_jsx(\_components.td, {\n children: \"submit\"\n })]\n })]\n })]\n }), \_jsxs(\_components.p, {\n children: [\"Finally, the \", \_jsx(InlineCode, {\n children: \".left\_edge\"\n }), \" and \", \_jsx(InlineCode, {\n children: \".right\_edge\"\n }), \" attributes can be especially useful,\\nbecause they give you the first and last token of the subtree. This is the\\neasiest way to create a \", \_jsx(InlineCode, {\n children: \"Span\"\n }), \" object for a syntactic phrase. Note that\\n\", \_jsx(InlineCode, {\n children: \".right\_edge\"\n }), \" gives a token \", \_jsx(\_components.strong, {\n children: \"within\"\n }), \" the subtree – so if you use it as the\\nend-point of a range, don’t forget to \", \_jsx(InlineCode, {\n children: \"+1\"\n }), \"!\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Credit and mortgage account holders must submit their requests\\\")\\nspan = doc[doc[4].left\_edge.i : doc[4].right\_edge.i+1]\\nwith doc.retokenize() as retokenizer:\\n retokenizer.merge(span)\\nfor token in doc:\\n print(token.text, token.pos\_, token.dep\_, token.head.text)\\n\"\n })\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Text\"\n }), \_jsx(\_components.th, {\n children: \"POS\"\n }), \_jsx(\_components.th, {\n children: \"Dep\"\n }), \_jsx(\_components.th, {\n children: \"Head text\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"Credit and mortgage account holders\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"NOUN\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"nsubj\"\n })\n }), \_jsx(\_components.td, {\n children: \"submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"must\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"aux\"\n })\n }), \_jsx(\_components.td, {\n children: \"submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"submit\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"VERB\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"ROOT\"\n })\n }), \_jsx(\_components.td, {\n children: \"submit\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"their\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"ADJ\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"poss\"\n })\n }), \_jsx(\_components.td, {\n children: \"requests\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"requests\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"NOUN\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"dobj\"\n })\n }), \_jsx(\_components.td, {\n children: \"submit\"\n })]\n })]\n })]\n }), \_jsxs(\_components.p, {\n children: [\"The dependency parse can be a useful tool for \", \_jsx(\_components.strong, {\n children: \"information extraction\"\n }), \",\\nespecially when combined with other predictions like\\n\", \_jsx(\_components.a, {\n href: \"#named-entities\",\n children: \"named entities\"\n }), \". The following example extracts money and\\ncurrency values, i.e. entities labeled as \", \_jsx(InlineCode, {\n children: \"MONEY\"\n }), \", and then uses the dependency\\nparse to find the noun phrase they are referring to – for example \", \_jsx(InlineCode, {\n children: \"\\\"Net income\\\"\"\n }), \"\\n→ \", \_jsx(InlineCode, {\n children: \"\\\"$9.4 million\\\"\"\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\n# Merge noun phrases and entities for easier analysis\\nnlp.add\_pipe(\\\"merge\_entities\\\")\\nnlp.add\_pipe(\\\"merge\_noun\_chunks\\\")\\n\\nTEXTS = [\\n \\\"Net income was $9.4 million compared to the prior year of $2.7 million.\\\",\\n \\\"Revenue exceeded twelve billion dollars, with a loss of $1b.\\\",\\n]\\nfor doc in nlp.pipe(TEXTS):\\n for token in doc:\\n if token.ent\_type\_ == \\\"MONEY\\\":\\n # We have an attribute and direct object, so check for subject\\n if token.dep\_ in (\\\"attr\\\", \\\"dobj\\\"):\\n subj = [w for w in token.head.lefts if w.dep\_ == \\\"nsubj\\\"]\\n if subj:\\n print(subj[0], \\\"--\u003e\\\", token)\\n # We have a prepositional object with a preposition\\n elif token.dep\_ == \\\"pobj\\\" and token.head.dep\_ == \\\"prep\\\":\\n print(token.head.head, \\\"--\u003e\\\", token)\\n\"\n })\n }), \_jsx(Infobox, {\n title: \"Combining models and rules\",\n emoji: \"📖\",\n children: \_jsxs(\_components.p, {\n children: [\"For more examples of how to write rule-based information extraction logic that\\ntakes advantage of the model’s predictions produced by the different components,\\nsee the usage guide on\\n\", \_jsx(\_components.a, {\n href: \"/usage/rule-based-matching#models-rules\",\n children: \"combining models and rules\"\n }), \".\"]\n })\n }), \_jsx(\_components.h3, {\n id: \"displacy\",\n children: \"Visualizing dependencies \"\n }), \_jsxs(\_components.p, {\n children: [\"The best way to understand spaCy’s dependency parser is interactively. To make\\nthis easier, spaCy comes with a visualization module. You can pass a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" or a\\nlist of \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" objects to displaCy and run\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#displacy.serve\",\n children: \_jsx(InlineCode, {\n children: \"displacy.serve\"\n })\n }), \" to run the web server, or\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#displacy.render\",\n children: \_jsx(InlineCode, {\n children: \"displacy.render\"\n })\n }), \" to generate the raw markup.\\nIf you want to know how to write rules that hook into some type of syntactic\\nconstruction, just plug the sentence into the visualizer and see how spaCy\\nannotates it.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy import displacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"Autonomous cars shift insurance liability toward manufacturers\\\")\\n# Since this is an interactive Jupyter environment, we can use displacy.render here\\ndisplacy.render(doc, style='dep')\\n\"\n })\n }), \_jsx(Infobox, {\n children: \_jsxs(\_components.p, {\n children: [\"For more details and examples, see the\\n\", \_jsx(\_components.a, {\n href: \"/usage/visualizers\",\n children: \"usage guide on visualizing spaCy\"\n }), \". You can also test\\ndisplaCy in our \", \_jsx(\_components.a, {\n href: \"https://explosion.ai/demos/displacy\",\n children: \"online demo\"\n }), \"..\"]\n })\n }), \_jsx(\_components.h3, {\n id: \"disabling\",\n children: \"Disabling the parser \"\n }), \_jsxs(\_components.p, {\n children: [\"In the \", \_jsx(\_components.a, {\n href: \"/models\",\n children: \"trained pipelines\"\n }), \" provided by spaCy, the parser is loaded and\\nenabled by default as part of the\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines\",\n children: \"standard processing pipeline\"\n }), \". If you don’t need\\nany of the syntactic information, you should disable the parser. Disabling the\\nparser will make spaCy load and run much faster. If you want to load the parser,\\nbut need to disable it for specific documents, you can also control its use on\\nthe \", \_jsx(InlineCode, {\n children: \"nlp\"\n }), \" object. For more details, see the usage guide on\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines/#disabling\",\n children: \"disabling pipeline components\"\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"nlp = spacy.load(\\\"en\_core\_web\_sm\\\", disable=[\\\"parser\\\"])\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-named-entities\",\n children: [\_jsx(\_components.h2, {\n id: \"named-entities\",\n children: \"Named Entity Recognition \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy features an extremely fast statistical entity recognition system, that\\nassigns labels to contiguous spans of tokens. The default\\n\", \_jsx(\_components.a, {\n href: \"/models\",\n children: \"trained pipelines\"\n }), \" can identify a variety of named and numeric\\nentities, including companies, locations, organizations and products. You can\\nadd arbitrary classes to the entity recognition system, and update the model\\nwith new examples.\"]\n }), \_jsx(\_components.h3, {\n id: \"named-entities-101\",\n children: \"Named Entity Recognition 101 \"\n }), \_jsx(NER101, {}), \_jsx(\_components.h3, {\n id: \"accessing-ner\",\n children: \"Accessing entity annotations and labels \"\n }), \_jsxs(\_components.p, {\n children: [\"The standard way to access entity annotations is the \", \_jsx(\_components.a, {\n href: \"/api/doc#ents\",\n children: \_jsx(InlineCode, {\n children: \"doc.ents\"\n })\n }), \"\\nproperty, which produces a sequence of \", \_jsx(\_components.a, {\n href: \"/api/span\",\n children: \_jsx(InlineCode, {\n children: \"Span\"\n })\n }), \" objects. The entity\\ntype is accessible either as a hash value or as a string, using the attributes\\n\", \_jsx(InlineCode, {\n children: \"ent.label\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"ent.label\_\"\n }), \". The \", \_jsx(InlineCode, {\n children: \"Span\"\n }), \" object acts as a sequence of tokens, so\\nyou can iterate over the entity or index into it. You can also get the text form\\nof the whole entity, as though it were a single token.\"]\n }), \_jsxs(\_components.p, {\n children: [\"You can also access token entity annotations using the\\n\", \_jsx(\_components.a, {\n href: \"/api/token#attributes\",\n children: \_jsx(InlineCode, {\n children: \"token.ent\_iob\"\n })\n }), \" and\\n\", \_jsx(\_components.a, {\n href: \"/api/token#attributes\",\n children: \_jsx(InlineCode, {\n children: \"token.ent\_type\"\n })\n }), \" attributes. \", \_jsx(InlineCode, {\n children: \"token.ent\_iob\"\n }), \" indicates\\nwhether an entity starts, continues or ends on the tag. If no entity type is set\\non a token, it will return an empty string.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"IOB Scheme\"\n }), \"\\n\", \_jsxs(\_components.ul, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"I\"\n }), \" – Token is \", \_jsx(\_components.strong, {\n children: \"inside\"\n }), \" an entity.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"O\"\n }), \" – Token is \", \_jsx(\_components.strong, {\n children: \"outside\"\n }), \" an entity.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"B\"\n }), \" – Token is the \", \_jsx(\_components.strong, {\n children: \"beginning\"\n }), \" of an entity.\"]\n }), \"\\n\"]\n }), \"\\n\", \_jsx(\_components.h4, {\n children: \"BILUO Scheme\"\n }), \"\\n\", \_jsxs(\_components.ul, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"B\"\n }), \" – Token is the \", \_jsx(\_components.strong, {\n children: \"beginning\"\n }), \" of a multi-token entity.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"I\"\n }), \" – Token is \", \_jsx(\_components.strong, {\n children: \"inside\"\n }), \" a multi-token entity.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"L\"\n }), \" – Token is the \", \_jsx(\_components.strong, {\n children: \"last\"\n }), \" token of a multi-token entity.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"U\"\n }), \" – Token is a single-token \", \_jsx(\_components.strong, {\n children: \"unit\"\n }), \" entity.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"O\"\n }), \" – Token is \", \_jsx(\_components.strong, {\n children: \"outside\"\n }), \" an entity.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"San Francisco considers banning sidewalk delivery robots\\\")\\n\\n# document level\\nents = [(e.text, e.start\_char, e.end\_char, e.label\_) for e in doc.ents]\\nprint(ents)\\n\\n# token level\\nent\_san = [doc[0].text, doc[0].ent\_iob\_, doc[0].ent\_type\_]\\nent\_francisco = [doc[1].text, doc[1].ent\_iob\_, doc[1].ent\_type\_]\\nprint(ent\_san) # ['San', 'B', 'GPE']\\nprint(ent\_francisco) # ['Francisco', 'I', 'GPE']\\n\"\n })\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Text\"\n }), \_jsx(\_components.th, {\n children: \"ent\_iob\"\n }), \_jsx(\_components.th, {\n children: \"ent\_iob\_\"\n }), \_jsx(\_components.th, {\n children: \"ent\_type\_\"\n }), \_jsx(\_components.th, {\n children: \"Description\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"San\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"3\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"B\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"GPE\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"beginning of an entity\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"Francisco\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"1\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"I\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"GPE\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"inside an entity\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"considers\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"2\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"O\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"outside an entity\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"banning\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"2\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"O\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"outside an entity\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"sidewalk\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"2\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"O\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"outside an entity\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"delivery\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"2\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"O\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"outside an entity\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \"robots\"\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"2\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"O\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \"outside an entity\"\n })]\n })]\n })]\n }), \_jsx(\_components.h3, {\n id: \"setting-entities\",\n children: \"Setting entity annotations \"\n }), \_jsxs(\_components.p, {\n children: [\"To ensure that the sequence of token annotations remains consistent, you have to\\nset entity annotations \", \_jsx(\_components.strong, {\n children: \"at the document level\"\n }), \". However, you can’t write\\ndirectly to the \", \_jsx(InlineCode, {\n children: \"token.ent\_iob\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"token.ent\_type\"\n }), \" attributes, so the easiest\\nway to set entities is to use the \", \_jsx(\_components.a, {\n href: \"/api/doc#set\_ents\",\n children: \_jsx(InlineCode, {\n children: \"doc.set\_ents\"\n })\n }), \" function\\nand create the new entity as a \", \_jsx(\_components.a, {\n href: \"/api/span\",\n children: \_jsx(InlineCode, {\n children: \"Span\"\n })\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.tokens import Span\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"fb is hiring a new vice president of global policy\\\")\\nents = [(e.text, e.start\_char, e.end\_char, e.label\_) for e in doc.ents]\\nprint('Before', ents)\\n# The model didn't recognize \\\"fb\\\" as an entity :(\\n\\n# Create a span for the new entity\\nfb\_ent = Span(doc, 0, 1, label=\\\"ORG\\\")\\norig\_ents = list(doc.ents)\\n\\n# Option 1: Modify the provided entity spans, leaving the rest unmodified\\ndoc.set\_ents([fb\_ent], default=\\\"unmodified\\\")\\n\\n# Option 2: Assign a complete list of ents to doc.ents\\ndoc.ents = orig\_ents + [fb\_ent]\\n\\nents = [(e.text, e.start, e.end, e.label\_) for e in doc.ents]\\nprint('After', ents)\\n# [('fb', 0, 1, 'ORG')] 🎉\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"Keep in mind that \", \_jsx(InlineCode, {\n children: \"Span\"\n }), \" is initialized with the start and end \", \_jsx(\_components.strong, {\n children: \"token\"\n }), \"\\nindices, not the character offsets. To create a span from character offsets, use\\n\", \_jsx(\_components.a, {\n href: \"/api/doc#char\_span\",\n children: \_jsx(InlineCode, {\n children: \"Doc.char\_span\"\n })\n }), \":\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"fb\_ent = doc.char\_span(0, 2, label=\\\"ORG\\\")\\n\"\n })\n }), \_jsx(\_components.h4, {\n id: \"setting-from-array\",\n children: \"Setting entity annotations from array \"\n }), \_jsxs(\_components.p, {\n children: [\"You can also assign entity annotations using the\\n\", \_jsx(\_components.a, {\n href: \"/api/doc#from\_array\",\n children: \_jsx(InlineCode, {\n children: \"doc.from\_array\"\n })\n }), \" method. To do this, you should include\\nboth the \", \_jsx(InlineCode, {\n children: \"ENT\_TYPE\"\n }), \" and the \", \_jsx(InlineCode, {\n children: \"ENT\_IOB\"\n }), \" attributes in the array you’re importing\\nfrom.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import numpy\\nimport spacy\\nfrom spacy.attrs import ENT\_IOB, ENT\_TYPE\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp.make\_doc(\\\"London is a big city in the United Kingdom.\\\")\\nprint(\\\"Before\\\", doc.ents) # []\\n\\nheader = [ENT\_IOB, ENT\_TYPE]\\nattr\_array = numpy.zeros((len(doc), len(header)), dtype=\\\"uint64\\\")\\nattr\_array[0, 0] = 3 # B\\nattr\_array[0, 1] = doc.vocab.strings[\\\"GPE\\\"]\\ndoc.from\_array(header, attr\_array)\\nprint(\\\"After\\\", doc.ents) # [London]\\n\"\n })\n }), \_jsx(\_components.h4, {\n id: \"setting-cython\",\n children: \"Setting entity annotations in Cython \"\n }), \_jsxs(\_components.p, {\n children: [\"Finally, you can always write to the underlying struct if you compile a\\n\", \_jsx(\_components.a, {\n href: \"http://cython.org/\",\n children: \"Cython\"\n }), \" function. This is easy to do, and allows you to\\nwrite efficient native code.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"# cython: infer\_types=True\\nfrom spacy.typedefs cimport attr\_t\\nfrom spacy.tokens.doc cimport Doc\\n\\ncpdef set\_entity(Doc doc, int start, int end, attr\_t ent\_type):\\n for i in range(start, end):\\n doc.c[i].ent\_type = ent\_type\\n doc.c[start].ent\_iob = 3\\n for i in range(start+1, end):\\n doc.c[i].ent\_iob = 2\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"Obviously, if you write directly to the array of \", \_jsx(InlineCode, {\n children: \"TokenC\*\"\n }), \" structs, you’ll have\\nresponsibility for ensuring that the data is left in a consistent state.\"]\n }), \_jsx(\_components.h3, {\n id: \"entity-types\",\n children: \"Built-in entity types \"\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Tip: Understanding entity types\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"You can also use \", \_jsx(InlineCode, {\n children: \"spacy.explain()\"\n }), \" to get the description for the string\\nrepresentation of an entity label. For example, \", \_jsx(InlineCode, {\n children: \"spacy.explain(\\\"LANGUAGE\\\")\"\n }), \"\\nwill return “any named language”.\"]\n }), \"\\n\"]\n }), \_jsx(Infobox, {\n title: \"Annotation scheme\",\n children: \_jsxs(\_components.p, {\n children: [\"For details on the entity types available in spaCy’s trained pipelines, see the\\n“label scheme” sections of the individual models in the\\n\", \_jsx(\_components.a, {\n href: \"/models\",\n children: \"models directory\"\n }), \".\"]\n })\n }), \_jsx(\_components.h3, {\n id: \"displacy\",\n children: \"Visualizing named entities \"\n }), \_jsxs(\_components.p, {\n children: [\"The\\n\", \_jsxs(\_components.a, {\n href: \"https://explosion.ai/demos/displacy-ent\",\n children: [\"displaCy \", \_jsx(\"sup\", {\n children: \"ENT\"\n }), \" visualizer\"]\n }), \"\\nlets you explore an entity recognition model’s behavior interactively. If you’re\\ntraining a model, it’s very useful to run the visualization yourself. To help\\nyou do that, spaCy comes with a visualization module. You can pass a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" or a\\nlist of \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" objects to displaCy and run\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#displacy.serve\",\n children: \_jsx(InlineCode, {\n children: \"displacy.serve\"\n })\n }), \" to run the web server, or\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#displacy.render\",\n children: \_jsx(InlineCode, {\n children: \"displacy.render\"\n })\n }), \" to generate the raw markup.\"]\n }), \_jsxs(\_components.p, {\n children: [\"For more details and examples, see the\\n\", \_jsx(\_components.a, {\n href: \"/usage/visualizers\",\n children: \"usage guide on visualizing spaCy\"\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"Named Entity example\",\n children: \"import spacy\\nfrom spacy import displacy\\n\\ntext = \\\"When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.\\\"\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(text)\\ndisplacy.serve(doc, style=\\\"ent\\\")\\n\"\n })\n }), \_jsx(Standalone, {\n height: 180,\n children: \_jsxs(\"div\", {\n style: {\n lineHeight: 2.5,\n fontFamily: \"-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'\",\n fontSize: 18\n },\n children: [\"When \", \_jsxs(\"mark\", {\n style: {\n background: '#aa9cfc',\n padding: '0.45em 0.6em',\n margin: '0 0.25em',\n lineHeight: 1,\n borderRadius: '0.35em'\n },\n children: [\"Sebastian Thrun \", \_jsx(\"span\", {\n style: {\n fontSize: '0.8em',\n fontWeight: 'bold',\n lineHeight: 1,\n borderRadius: '0.35em',\n marginLeft: '0.5rem'\n },\n children: \"PERSON\"\n })]\n }), \" started working on self-driving cars at \", \_jsxs(\"mark\", {\n style: {\n background: '#7aecec',\n padding: '0.45em 0.6em',\n margin: '0 0.25em',\n lineHeight: 1,\n borderRadius: '0.35em'\n },\n children: [\"Google \", \_jsx(\"span\", {\n style: {\n fontSize: '0.8em',\n fontWeight: 'bold',\n lineHeight: 1,\n borderRadius: '0.35em',\n marginLeft: '0.5rem'\n },\n children: \"ORG\"\n })]\n }), \" in \", \_jsxs(\"mark\", {\n style: {\n background: '#bfe1d9',\n padding: '0.45em 0.6em',\n margin: '0 0.25em',\n lineHeight: 1,\n borderRadius: '0.35em'\n },\n children: [\"2007 \", \_jsx(\"span\", {\n style: {\n fontSize: '0.8em',\n fontWeight: 'bold',\n lineHeight: 1,\n borderRadius: '0.35em',\n marginLeft: '0.5rem'\n },\n children: \"DATE\"\n })]\n }), \", few people outside of the company took him seriously.\"]\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-entity-linking\",\n children: [\_jsx(\_components.h2, {\n id: \"entity-linking\",\n children: \"Entity Linking \"\n }), \_jsxs(\_components.p, {\n children: [\"To ground the named entities into the “real world”, spaCy provides functionality\\nto perform entity linking, which resolves a textual entity to a unique\\nidentifier from a knowledge base (KB). You can create your own\\n\", \_jsx(\_components.a, {\n href: \"/api/kb\",\n children: \_jsx(InlineCode, {\n children: \"KnowledgeBase\"\n })\n }), \" and \", \_jsx(\_components.a, {\n href: \"/usage/training\",\n children: \"train\"\n }), \" a new\\n\", \_jsx(\_components.a, {\n href: \"/api/entitylinker\",\n children: \_jsx(InlineCode, {\n children: \"EntityLinker\"\n })\n }), \" using that custom knowledge base.\"]\n }), \_jsxs(\_components.p, {\n children: [\"As an example on how to define a KnowledgeBase and train an entity linker model,\\nsee \", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/projects/blob/v3/tutorials/nel\_emerson\",\n children: \_jsx(InlineCode, {\n children: \"this tutorial\"\n })\n }), \"\\nusing \", \_jsx(\_components.a, {\n href: \"/usage/projects\",\n children: \"spaCy projects\"\n }), \".\"]\n }), \_jsx(\_components.h3, {\n id: \"entity-linking-accessing\",\n model: \"entity linking\",\n children: \"Accessing entity identifiers \"\n }), \_jsxs(\_components.p, {\n children: [\"The annotated KB identifier is accessible as either a hash value or as a string,\\nusing the attributes \", \_jsx(InlineCode, {\n children: \"ent.kb\_id\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"ent.kb\_id\_\"\n }), \" of a \", \_jsx(\_components.a, {\n href: \"/api/span\",\n children: \_jsx(InlineCode, {\n children: \"Span\"\n })\n }), \"\\nobject, or the \", \_jsx(InlineCode, {\n children: \"ent\_kb\_id\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"ent\_kb\_id\_\"\n }), \" attributes of a\\n\", \_jsx(\_components.a, {\n href: \"/api/token\",\n children: \_jsx(InlineCode, {\n children: \"Token\"\n })\n }), \" object.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"import spacy\\n\\n# \\\"my\_custom\_el\_pipeline\\\" is assumed to be a custom NLP pipeline that was trained and serialized to disk\\nnlp = spacy.load(\\\"my\_custom\_el\_pipeline\\\")\\ndoc = nlp(\\\"Ada Lovelace was born in London\\\")\\n\\n# Document level\\nents = [(e.text, e.label\_, e.kb\_id\_) for e in doc.ents]\\nprint(ents) # [('Ada Lovelace', 'PERSON', 'Q7259'), ('London', 'GPE', 'Q84')]\\n\\n# Token level\\nent\_ada\_0 = [doc[0].text, doc[0].ent\_type\_, doc[0].ent\_kb\_id\_]\\nent\_ada\_1 = [doc[1].text, doc[1].ent\_type\_, doc[1].ent\_kb\_id\_]\\nent\_london\_5 = [doc[5].text, doc[5].ent\_type\_, doc[5].ent\_kb\_id\_]\\nprint(ent\_ada\_0) # ['Ada', 'PERSON', 'Q7259']\\nprint(ent\_ada\_1) # ['Lovelace', 'PERSON', 'Q7259']\\nprint(ent\_london\_5) # ['London', 'GPE', 'Q84']\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-tokenization\",\n children: [\_jsx(\_components.h2, {\n id: \"tokenization\",\n children: \"Tokenization \"\n }), \_jsxs(\_components.p, {\n children: [\"Tokenization is the task of splitting a text into meaningful segments, called\\n\", \_jsx(\_components.em, {\n children: \"tokens\"\n }), \". The input to the tokenizer is a unicode text, and the output is a\\n\", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object. To construct a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" object, you need a\\n\", \_jsx(\_components.a, {\n href: \"/api/vocab\",\n children: \_jsx(InlineCode, {\n children: \"Vocab\"\n })\n }), \" instance, a sequence of \", \_jsx(InlineCode, {\n children: \"word\"\n }), \" strings, and optionally a\\nsequence of \", \_jsx(InlineCode, {\n children: \"spaces\"\n }), \" booleans, which allow you to maintain alignment of the\\ntokens into the original string.\"]\n }), \_jsx(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"spaCy’s tokenization is \", \_jsx(\_components.strong, {\n children: \"non-destructive\"\n }), \", which means that you’ll always be\\nable to reconstruct the original input from the tokenized output. Whitespace\\ninformation is preserved in the tokens and no information is added or removed\\nduring tokenization. This is kind of a core principle of spaCy’s \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" object:\\n\", \_jsx(InlineCode, {\n children: \"doc.text == input\_text\"\n }), \" should always hold true.\"]\n })\n }), \_jsx(Tokenization101, {}), \_jsxs(Accordion, {\n title: \"Algorithm details: How spaCy's tokenizer works\",\n id: \"how-tokenizer-works\",\n spaced: true,\n children: [\_jsx(\_components.p, {\n children: \"spaCy introduces a novel tokenization algorithm that gives a better balance\\nbetween performance, ease of definition and ease of alignment into the original\\nstring.\"\n }), \_jsx(\_components.p, {\n children: \"After consuming a prefix or suffix, we consult the special cases again. We want\\nthe special cases to handle things like “don’t” in English, and we want the same\\nrule to work for “(don’t)!“. We do this by splitting off the open bracket, then\\nthe exclamation, then the closed bracket, and finally matching the special case.\\nHere’s an implementation of the algorithm in Python optimized for readability\\nrather than performance:\"\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"def tokenizer\_pseudo\_code(\\n text,\\n special\_cases,\\n prefix\_search,\\n suffix\_search,\\n infix\_finditer,\\n token\_match,\\n url\_match\\n):\\n tokens = []\\n for substring in text.split():\\n suffixes = []\\n while substring:\\n if substring in special\_cases:\\n tokens.extend(special\_cases[substring])\\n substring = \\\"\\\"\\n continue\\n while prefix\_search(substring) or suffix\_search(substring):\\n if token\_match(substring):\\n tokens.append(substring)\\n substring = \\\"\\\"\\n break\\n if substring in special\_cases:\\n tokens.extend(special\_cases[substring])\\n substring = \\\"\\\"\\n break\\n if prefix\_search(substring):\\n split = prefix\_search(substring).end()\\n tokens.append(substring[:split])\\n substring = substring[split:]\\n if substring in special\_cases:\\n continue\\n if suffix\_search(substring):\\n split = suffix\_search(substring).start()\\n suffixes.append(substring[split:])\\n substring = substring[:split]\\n if token\_match(substring):\\n tokens.append(substring)\\n substring = \\\"\\\"\\n elif url\_match(substring):\\n tokens.append(substring)\\n substring = \\\"\\\"\\n elif substring in special\_cases:\\n tokens.extend(special\_cases[substring])\\n substring = \\\"\\\"\\n elif list(infix\_finditer(substring)):\\n infixes = infix\_finditer(substring)\\n offset = 0\\n for match in infixes:\\n if offset == 0 and match.start() == 0:\\n continue\\n tokens.append(substring[offset : match.start()])\\n tokens.append(substring[match.start() : match.end()])\\n offset = match.end()\\n if substring[offset:]:\\n tokens.append(substring[offset:])\\n substring = \\\"\\\"\\n elif substring:\\n tokens.append(substring)\\n substring = \\\"\\\"\\n tokens.extend(reversed(suffixes))\\n for match in matcher(special\_cases, text):\\n tokens.replace(match, special\_cases[match])\\n return tokens\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"The algorithm can be summarized as follows:\"\n }), \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsx(\_components.li, {\n children: \"Iterate over space-separated substrings.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Check whether we have an explicitly defined special case for this substring.\\nIf we do, use it.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Look for a token match. If there is a match, stop processing and keep this\\ntoken.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Check whether we have an explicitly defined special case for this substring.\\nIf we do, use it.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Otherwise, try to consume one prefix. If we consumed a prefix, go back to #3,\\nso that the token match and special cases always get priority.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"If we didn’t consume a prefix, try to consume a suffix and then go back to\\n#3.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"If we can’t consume a prefix or a suffix, look for a URL match.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"If there’s no URL match, then look for a special case.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Look for “infixes” – stuff like hyphens etc. and split the substring into\\ntokens on all infixes.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Once we can’t consume any more of the string, handle it as a single token.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Make a final pass over the text to check for special cases that include\\nspaces or that were missed due to the incremental processing of affixes.\"\n }), \"\\n\"]\n })]\n }), \_jsxs(\_components.p, {\n children: [\_jsx(\_components.strong, {\n children: \"Global\"\n }), \" and \", \_jsx(\_components.strong, {\n children: \"language-specific\"\n }), \" tokenizer data is supplied via the language\\ndata in \", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spaCy/tree/master/spacy/lang\",\n children: \_jsx(InlineCode, {\n children: \"spacy/lang\"\n })\n }), \". The tokenizer exceptions\\ndefine special cases like “don’t” in English, which needs to be split into two\\ntokens: \", \_jsx(InlineCode, {\n children: \"{ORTH: \\\"do\\\"}\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"{ORTH: \\\"n't\\\", NORM: \\\"not\\\"}\"\n }), \". The prefixes, suffixes\\nand infixes mostly define punctuation rules – for example, when to split off\\nperiods (at the end of a sentence), and when to leave tokens containing periods\\nintact (abbreviations like “U.S.”).\"]\n }), \_jsx(Accordion, {\n title: \"Should I change the language data or add custom tokenizer rules?\",\n id: \"lang-data-vs-tokenizer\",\n children: \_jsxs(\_components.p, {\n children: [\"Tokenization rules that are specific to one language, but can be \", \_jsx(\_components.strong, {\n children: \"generalized\\nacross that language\"\n }), \", should ideally live in the language data in\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spaCy/tree/master/spacy/lang\",\n children: \_jsx(InlineCode, {\n children: \"spacy/lang\"\n })\n }), \" – we always appreciate pull requests!\\nAnything that’s specific to a domain or text type – like financial trading\\nabbreviations or Bavarian youth slang – should be added as a special case rule\\nto your tokenizer instance. If you’re dealing with a lot of customizations, it\\nmight make sense to create an entirely custom subclass.\"]\n })\n }), \_jsx(\_components.hr, {}), \_jsx(\_components.h3, {\n id: \"special-cases\",\n children: \"Adding special case tokenization rules \"\n }), \_jsxs(\_components.p, {\n children: [\"Most domains have at least some idiosyncrasies that require custom tokenization\\nrules. This could be very certain expressions, or abbreviations only used in\\nthis specific field. Here’s how to add a special case rule to an existing\\n\", \_jsx(\_components.a, {\n href: \"/api/tokenizer\",\n children: \_jsx(InlineCode, {\n children: \"Tokenizer\"\n })\n }), \" instance:\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.symbols import ORTH\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"gimme that\\\") # phrase to tokenize\\nprint([w.text for w in doc]) # ['gimme', 'that']\\n\\n# Add special case rule\\nspecial\_case = [{ORTH: \\\"gim\\\"}, {ORTH: \\\"me\\\"}]\\nnlp.tokenizer.add\_special\_case(\\\"gimme\\\", special\_case)\\n\\n# Check new tokenization\\nprint([w.text for w in nlp(\\\"gimme that\\\")]) # ['gim', 'me', 'that']\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"The special case doesn’t have to match an entire whitespace-delimited substring.\\nThe tokenizer will incrementally split off punctuation, and keep looking up the\\nremaining substring. The special case rules also have precedence over the\\npunctuation splitting.\"\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"assert \\\"gimme\\\" not in [w.text for w in nlp(\\\"gimme!\\\")]\\nassert \\\"gimme\\\" not in [w.text for w in nlp('(\\\"...gimme...?\\\")')]\\n\\nnlp.tokenizer.add\_special\_case(\\\"...gimme...?\\\", [{\\\"ORTH\\\": \\\"...gimme...?\\\"}])\\nassert len(nlp(\\\"...gimme...?\\\")) == 1\\n\"\n })\n }), \_jsx(\_components.h4, {\n id: \"tokenizer-debug\",\n version: \"2.2.3\",\n children: \"Debugging the tokenizer \"\n }), \_jsxs(\_components.p, {\n children: [\"A working implementation of the pseudo-code above is available for debugging as\\n\", \_jsx(\_components.a, {\n href: \"/api/tokenizer#explain\",\n children: \_jsx(InlineCode, {\n children: \"nlp.tokenizer.explain(text)\"\n })\n }), \". It returns a list of\\ntuples showing which tokenizer rule or pattern was matched for each token. The\\ntokens produced are identical to \", \_jsx(InlineCode, {\n children: \"nlp.tokenizer()\"\n }), \" except for whitespace tokens:\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Expected output\"\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n lang: \"none\",\n children: \"\\\" PREFIX\\nLet SPECIAL-1\\n's SPECIAL-2\\ngo TOKEN\\n! SUFFIX\\n\\\" SUFFIX\\n\"\n })\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"from spacy.lang.en import English\\n\\nnlp = English()\\ntext = '''\\\"Let's go!\\\"'''\\ndoc = nlp(text)\\ntok\_exp = nlp.tokenizer.explain(text)\\nassert [t.text for t in doc if not t.is\_space] == [t[1] for t in tok\_exp]\\nfor t in tok\_exp:\\n print(t[1], \\\"\\\\\\\\t\\\", t[0])\\n\"\n })\n }), \_jsx(\_components.h3, {\n id: \"native-tokenizers\",\n children: \"Customizing spaCy’s Tokenizer class \"\n }), \_jsx(\_components.p, {\n children: \"Let’s imagine you wanted to create a tokenizer for a new language or specific\\ndomain. There are six things you may need to define:\"\n }), \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"A dictionary of \", \_jsx(\_components.strong, {\n children: \"special cases\"\n }), \". This handles things like contractions,\\nunits of measurement, emoticons, certain abbreviations, etc.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"A function \", \_jsx(InlineCode, {\n children: \"prefix\_search\"\n }), \", to handle \", \_jsx(\_components.strong, {\n children: \"preceding punctuation\"\n }), \", such as open\\nquotes, open brackets, etc.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"A function \", \_jsx(InlineCode, {\n children: \"suffix\_search\"\n }), \", to handle \", \_jsx(\_components.strong, {\n children: \"succeeding punctuation\"\n }), \", such as\\ncommas, periods, close quotes, etc.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"A function \", \_jsx(InlineCode, {\n children: \"infix\_finditer\"\n }), \", to handle non-whitespace separators, such as\\nhyphens etc.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"An optional boolean function \", \_jsx(InlineCode, {\n children: \"token\_match\"\n }), \" matching strings that should never\\nbe split, overriding the infix rules. Useful for things like numbers.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"An optional boolean function \", \_jsx(InlineCode, {\n children: \"url\_match\"\n }), \", which is similar to \", \_jsx(InlineCode, {\n children: \"token\_match\"\n }), \"\\nexcept that prefixes and suffixes are removed before applying the match.\"]\n }), \"\\n\"]\n }), \_jsxs(\_components.p, {\n children: [\"You shouldn’t usually need to create a \", \_jsx(InlineCode, {\n children: \"Tokenizer\"\n }), \" subclass. Standard usage is\\nto use \", \_jsx(InlineCode, {\n children: \"re.compile()\"\n }), \" to build a regular expression object, and pass its\\n\", \_jsx(InlineCode, {\n children: \".search()\"\n }), \" and \", \_jsx(InlineCode, {\n children: \".finditer()\"\n }), \" methods:\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import re\\nimport spacy\\nfrom spacy.tokenizer import Tokenizer\\n\\nspecial\_cases = {\\\":)\\\": [{\\\"ORTH\\\": \\\":)\\\"}]}\\nprefix\_re = re.compile(r'''^[\\\\\\\\[\\\\\\\\(\\\"']''')\\nsuffix\_re = re.compile(r'''[\\\\\\\\]\\\\\\\\)\\\"']$''')\\ninfix\_re = re.compile(r'''[-~]''')\\nsimple\_url\_re = re.compile(r'''^https?://''')\\n\\ndef custom\_tokenizer(nlp):\\n return Tokenizer(nlp.vocab, rules=special\_cases,\\n prefix\_search=prefix\_re.search,\\n suffix\_search=suffix\_re.search,\\n infix\_finditer=infix\_re.finditer,\\n url\_match=simple\_url\_re.match)\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\nnlp.tokenizer = custom\_tokenizer(nlp)\\ndoc = nlp(\\\"hello-world. :)\\\")\\nprint([t.text for t in doc]) # ['hello', '-', 'world.', ':)']\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"If you need to subclass the tokenizer instead, the relevant methods to\\nspecialize are \", \_jsx(InlineCode, {\n children: \"find\_prefix\"\n }), \", \", \_jsx(InlineCode, {\n children: \"find\_suffix\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"find\_infix\"\n }), \".\"]\n }), \_jsx(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"When customizing the prefix, suffix and infix handling, remember that you’re\\npassing in \", \_jsx(\_components.strong, {\n children: \"functions\"\n }), \" for spaCy to execute, e.g. \", \_jsx(InlineCode, {\n children: \"prefix\_re.search\"\n }), \" – not\\njust the regular expressions. This means that your functions also need to define\\nhow the rules should be applied. For example, if you’re adding your own prefix\\nrules, you need to make sure they’re only applied to characters at the\\n\", \_jsx(\_components.strong, {\n children: \"beginning of a token\"\n }), \", e.g. by adding \", \_jsx(InlineCode, {\n children: \"^\"\n }), \". Similarly, suffix rules should\\nonly be applied at the \", \_jsx(\_components.strong, {\n children: \"end of a token\"\n }), \", so your expression should end with a\\n\", \_jsx(InlineCode, {\n children: \"$\"\n }), \".\"]\n })\n }), \_jsx(\_components.h4, {\n id: \"native-tokenizer-additions\",\n children: \"Modifying existing rule sets \"\n }), \_jsxs(\_components.p, {\n children: [\"In many situations, you don’t necessarily need entirely custom rules. Sometimes\\nyou just want to add another character to the prefixes, suffixes or infixes. The\\ndefault prefix, suffix and infix rules are available via the \", \_jsx(InlineCode, {\n children: \"nlp\"\n }), \" object’s\\n\", \_jsx(InlineCode, {\n children: \"Defaults\"\n }), \" and the \", \_jsx(InlineCode, {\n children: \"Tokenizer\"\n }), \" attributes such as\\n\", \_jsx(\_components.a, {\n href: \"/api/tokenizer#attributes\",\n children: \_jsx(InlineCode, {\n children: \"Tokenizer.suffix\_search\"\n })\n }), \" are writable, so you can\\noverwrite them with compiled regular expression objects using modified default\\nrules. spaCy ships with utility functions to help you compile the regular\\nexpressions – for example,\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#util.compile\_suffix\_regex\",\n children: \_jsx(InlineCode, {\n children: \"compile\_suffix\_regex\"\n })\n }), \":\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"suffixes = nlp.Defaults.suffixes + [r'''-+$''',]\\nsuffix\_regex = spacy.util.compile\_suffix\_regex(suffixes)\\nnlp.tokenizer.suffix\_search = suffix\_regex.search\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"Similarly, you can remove a character from the default suffixes:\"\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"suffixes = list(nlp.Defaults.suffixes)\\nsuffixes.remove(\\\"\\\\\\\\\\\\\\\\[\\\")\\nsuffix\_regex = spacy.util.compile\_suffix\_regex(suffixes)\\nnlp.tokenizer.suffix\_search = suffix\_regex.search\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(InlineCode, {\n children: \"Tokenizer.suffix\_search\"\n }), \" attribute should be a function which takes a\\nunicode string and returns a \", \_jsx(\_components.strong, {\n children: \"regex match object\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"None\"\n }), \". Usually we use\\nthe \", \_jsx(InlineCode, {\n children: \".search\"\n }), \" attribute of a compiled regex object, but you can use some other\\nfunction that behaves the same way.\"]\n }), \_jsx(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"If you’ve loaded a trained pipeline, writing to the\\n\", \_jsx(\_components.a, {\n href: \"/api/language#defaults\",\n children: \_jsx(InlineCode, {\n children: \"nlp.Defaults\"\n })\n }), \" or \", \_jsx(InlineCode, {\n children: \"English.Defaults\"\n }), \" directly won’t\\nwork, since the regular expressions are read from the pipeline data and will be\\ncompiled when you load it. If you modify \", \_jsx(InlineCode, {\n children: \"nlp.Defaults\"\n }), \", you’ll only see the\\neffect if you call \", \_jsx(\_components.a, {\n href: \"/api/top-level#spacy.blank\",\n children: \_jsx(InlineCode, {\n children: \"spacy.blank\"\n })\n }), \". If you want to\\nmodify the tokenizer loaded from a trained pipeline, you should modify\\n\", \_jsx(InlineCode, {\n children: \"nlp.tokenizer\"\n }), \" directly. If you’re training your own pipeline, you can register\\n\", \_jsx(\_components.a, {\n href: \"/usage/training/#custom-code-nlp-callbacks\",\n children: \"callbacks\"\n }), \" to modify the \", \_jsx(InlineCode, {\n children: \"nlp\"\n }), \"\\nobject before training.\"]\n })\n }), \_jsxs(\_components.p, {\n children: [\"The prefix, infix and suffix rule sets include not only individual characters\\nbut also detailed regular expressions that take the surrounding context into\\naccount. For example, there is a regular expression that treats a hyphen between\\nletters as an infix. If you do not want the tokenizer to split on hyphens\\nbetween letters, you can modify the existing infix definition from\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py\",\n children: \_jsx(InlineCode, {\n children: \"lang/punctuation.py\"\n })\n }), \":\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.lang.char\_classes import ALPHA, ALPHA\_LOWER, ALPHA\_UPPER\\nfrom spacy.lang.char\_classes import CONCAT\_QUOTES, LIST\_ELLIPSES, LIST\_ICONS\\nfrom spacy.util import compile\_infix\_regex\\n\\n# Default tokenizer\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"mother-in-law\\\")\\nprint([t.text for t in doc]) # ['mother', '-', 'in', '-', 'law']\\n\\n# Modify tokenizer infix patterns\\ninfixes = (\\n LIST\_ELLIPSES\\n + LIST\_ICONS\\n + [\\n r\\\"(?\u003c=[0-9])[+\\\\\\\\-\\\\\\\\\*^](?=[0-9-])\\\",\\n r\\\"(?\u003c=[{al}{q}])\\\\\\\\.(?=[{au}{q}])\\\".format(\\n al=ALPHA\_LOWER, au=ALPHA\_UPPER, q=CONCAT\_QUOTES\\n ),\\n r\\\"(?\u003c=[{a}]),(?=[{a}])\\\".format(a=ALPHA),\\n # ✅ Commented out regex that splits on hyphens between letters:\\n # r\\\"(?\u003c=[{a}])(?:{h})(?=[{a}])\\\".format(a=ALPHA, h=HYPHENS),\\n r\\\"(?\u003c=[{a}0-9])[:\u003c\u003e=/](?=[{a}])\\\".format(a=ALPHA),\\n ]\\n)\\n\\ninfix\_re = compile\_infix\_regex(infixes)\\nnlp.tokenizer.infix\_finditer = infix\_re.finditer\\ndoc = nlp(\\\"mother-in-law\\\")\\nprint([t.text for t in doc]) # ['mother-in-law']\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"For an overview of the default regular expressions, see\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spaCy/tree/master/spacy/lang/punctuation.py\",\n children: \_jsx(InlineCode, {\n children: \"lang/punctuation.py\"\n })\n }), \" and\\nlanguage-specific definitions such as\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spaCy/tree/master/spacy/lang/de/punctuation.py\",\n children: \_jsx(InlineCode, {\n children: \"lang/de/punctuation.py\"\n })\n }), \" for\\nGerman.\"]\n }), \_jsx(\_components.h3, {\n id: \"custom-tokenizer\",\n children: \"Hooking a custom tokenizer into the pipeline \"\n }), \_jsxs(\_components.p, {\n children: [\"The tokenizer is the first component of the processing pipeline and the only one\\nthat can’t be replaced by writing to \", \_jsx(InlineCode, {\n children: \"nlp.pipeline\"\n }), \". This is because it has a\\ndifferent signature from all the other components: it takes a text and returns a\\n\", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \", whereas all other components expect to already receive a\\ntokenized \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \".\"]\n }), \_jsx(\_components.img, {\n src: \"/images/pipeline.svg\",\n alt: \"The processing pipeline\"\n }), \_jsxs(\_components.p, {\n children: [\"To overwrite the existing tokenizer, you need to replace \", \_jsx(InlineCode, {\n children: \"nlp.tokenizer\"\n }), \" with a\\ncustom function that takes a text and returns a \", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \".\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Creating a Doc\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"Constructing a \", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object manually requires at least two\\narguments: the shared \", \_jsx(InlineCode, {\n children: \"Vocab\"\n }), \" and a list of words. Optionally, you can pass in\\na list of \", \_jsx(InlineCode, {\n children: \"spaces\"\n }), \" values indicating whether the token at this position is\\nfollowed by a space (default \", \_jsx(InlineCode, {\n children: \"True\"\n }), \"). See the section on\\n\", \_jsx(\_components.a, {\n href: \"#own-annotations\",\n children: \"pre-tokenized text\"\n }), \" for more info.\"]\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"words = [\\\"Let\\\", \\\"'s\\\", \\\"go\\\", \\\"!\\\"]\\nspaces = [False, True, False, False]\\ndoc = Doc(nlp.vocab, words=words, spaces=spaces)\\n\"\n })\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"nlp = spacy.blank(\\\"en\\\")\\nnlp.tokenizer = my\_tokenizer\\n\"\n })\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Argument\"\n }), \_jsx(\_components.th, {\n children: \"Type\"\n }), \_jsx(\_components.th, {\n children: \"Description\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"text\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"str\"\n })\n }), \_jsx(\_components.td, {\n children: \"The raw text to tokenize.\"\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \_jsx(\_components.strong, {\n children: \"RETURNS\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n })\n }), \_jsx(\_components.td, {\n children: \"The tokenized document.\"\n })]\n })]\n })]\n }), \_jsx(\_components.h4, {\n id: \"custom-tokenizer-example\",\n children: \"Example 1: Basic whitespace tokenizer \"\n }), \_jsxs(\_components.p, {\n children: [\"Here’s an example of the most basic whitespace tokenizer. It takes the shared\\nvocab, so it can construct \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" objects. When it’s called on a text, it returns\\na \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" object consisting of the text split on single space characters. We can\\nthen overwrite the \", \_jsx(InlineCode, {\n children: \"nlp.tokenizer\"\n }), \" attribute with an instance of our custom\\ntokenizer.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.tokens import Doc\\n\\nclass WhitespaceTokenizer:\\n def \_\_init\_\_(self, vocab):\\n self.vocab = vocab\\n\\n def \_\_call\_\_(self, text):\\n words = text.split(\\\" \\\")\\n spaces = [True] \* len(words)\\n # Avoid zero-length tokens\\n for i, word in enumerate(words):\\n if word == \\\"\\\":\\n words[i] = \\\" \\\"\\n spaces[i] = False\\n # Remove the final trailing space\\n if words[-1] == \\\" \\\":\\n words = words[0:-1]\\n spaces = spaces[0:-1]\\n else:\\n spaces[-1] = False\\n\\n return Doc(self.vocab, words=words, spaces=spaces)\\n\\nnlp = spacy.blank(\\\"en\\\")\\nnlp.tokenizer = WhitespaceTokenizer(nlp.vocab)\\ndoc = nlp(\\\"What's happened to me? he thought. It wasn't a dream.\\\")\\nprint([token.text for token in doc])\\n\"\n })\n }), \_jsx(\_components.h4, {\n id: \"custom-tokenizer-example2\",\n children: \"Example 2: Third-party tokenizers (BERT word pieces) \"\n }), \_jsxs(\_components.p, {\n children: [\"You can use the same approach to plug in any other third-party tokenizers. Your\\ncustom callable just needs to return a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" object with the tokens produced by\\nyour tokenizer. In this example, the wrapper uses the \", \_jsx(\_components.strong, {\n children: \"BERT word piece\\ntokenizer\"\n }), \", provided by the\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/huggingface/tokenizers\",\n children: \_jsx(InlineCode, {\n children: \"tokenizers\"\n })\n }), \" library. The tokens\\navailable in the \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" object returned by spaCy now match the exact word pieces\\nproduced by the tokenizer.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"💡 Tip: spacy-transformers\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"If you’re working with transformer models like BERT, check out the\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/explosion/spacy-transformers\",\n children: \_jsx(InlineCode, {\n children: \"spacy-transformers\"\n })\n }), \"\\nextension package and \", \_jsx(\_components.a, {\n href: \"/usage/embeddings-transformers\",\n children: \"documentation\"\n }), \". It\\nincludes a pipeline component for using pretrained transformer weights and\\n\", \_jsx(\_components.strong, {\n children: \"training transformer models\"\n }), \" in spaCy, as well as helpful utilities for\\naligning word pieces to linguistic tokenization.\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"Custom BERT word piece tokenizer\",\n children: \"from tokenizers import BertWordPieceTokenizer\\nfrom spacy.tokens import Doc\\nimport spacy\\n\\nclass BertTokenizer:\\n def \_\_init\_\_(self, vocab, vocab\_file, lowercase=True):\\n self.vocab = vocab\\n self.\_tokenizer = BertWordPieceTokenizer(vocab\_file, lowercase=lowercase)\\n\\n def \_\_call\_\_(self, text):\\n tokens = self.\_tokenizer.encode(text)\\n words = []\\n spaces = []\\n for i, (text, (start, end)) in enumerate(zip(tokens.tokens, tokens.offsets)):\\n words.append(text)\\n if i \u003c len(tokens.tokens) - 1:\\n # If next start != current end we assume a space in between\\n next\_start, next\_end = tokens.offsets[i + 1]\\n spaces.append(next\_start \u003e end)\\n else:\\n spaces.append(True)\\n return Doc(self.vocab, words=words, spaces=spaces)\\n\\nnlp = spacy.blank(\\\"en\\\")\\nnlp.tokenizer = BertTokenizer(nlp.vocab, \\\"bert-base-uncased-vocab.txt\\\")\\ndoc = nlp(\\\"Justin Drew Bieber is a Canadian singer, songwriter, and actor.\\\")\\nprint(doc.text, [token.text for token in doc])\\n# [CLS]justin drew bi##eber is a canadian singer, songwriter, and actor.[SEP]\\n# ['[CLS]', 'justin', 'drew', 'bi', '##eber', 'is', 'a', 'canadian', 'singer',\\n# ',', 'songwriter', ',', 'and', 'actor', '.', '[SEP]']\\n\"\n })\n }), \_jsx(Infobox, {\n title: \"Important note on tokenization and models\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"Keep in mind that your models’ results may be less accurate if the tokenization\\nduring training differs from the tokenization at runtime. So if you modify a\\ntrained pipeline’s tokenization afterwards, it may produce very different\\npredictions. You should therefore train your pipeline with the \", \_jsx(\_components.strong, {\n children: \"same\\ntokenizer\"\n }), \" it will be using at runtime. See the docs on\\n\", \_jsx(\_components.a, {\n href: \"#custom-tokenizer-training\",\n children: \"training with custom tokenization\"\n }), \" for details.\"]\n })\n }), \_jsx(\_components.h4, {\n id: \"custom-tokenizer-training\",\n version: \"3\",\n children: \"Training with custom tokenization \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy’s \", \_jsx(\_components.a, {\n href: \"/usage/training#config\",\n children: \"training config\"\n }), \" describes the settings,\\nhyperparameters, pipeline and tokenizer used for constructing and training the\\npipeline. The \", \_jsx(InlineCode, {\n children: \"[nlp.tokenizer]\"\n }), \" block refers to a \", \_jsx(\_components.strong, {\n children: \"registered function\"\n }), \" that\\ntakes the \", \_jsx(InlineCode, {\n children: \"nlp\"\n }), \" object and returns a tokenizer. Here, we’re registering a\\nfunction called \", \_jsx(InlineCode, {\n children: \"whitespace\_tokenizer\"\n }), \" in the\\n\", \_jsxs(\_components.a, {\n href: \"/api/top-level#registry\",\n children: [\_jsx(InlineCode, {\n children: \"@tokenizers\"\n }), \" registry\"]\n }), \". To make sure spaCy knows how\\nto construct your tokenizer during training, you can pass in your Python file by\\nsetting \", \_jsx(InlineCode, {\n children: \"--code functions.py\"\n }), \" when you run \", \_jsx(\_components.a, {\n href: \"/api/cli#train\",\n children: \_jsx(InlineCode, {\n children: \"spacy train\"\n })\n }), \".\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"config.cfg\"\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-ini\",\n lang: \"ini\",\n children: \"[nlp.tokenizer]\\n@tokenizers = \\\"whitespace\_tokenizer\\\"\\n\"\n })\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"functions.py\",\n highlight: \"1\",\n children: \"@spacy.registry.tokenizers(\\\"whitespace\_tokenizer\\\")\\ndef create\_whitespace\_tokenizer():\\n def create\_tokenizer(nlp):\\n return WhitespaceTokenizer(nlp.vocab)\\n\\n return create\_tokenizer\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"Registered functions can also take arguments that are then passed in from the\\nconfig. This allows you to quickly change and keep track of different settings.\\nHere, the registered function called \", \_jsx(InlineCode, {\n children: \"bert\_word\_piece\_tokenizer\"\n }), \" takes two\\narguments: the path to a vocabulary file and whether to lowercase the text. The\\nPython type hints \", \_jsx(InlineCode, {\n children: \"str\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"bool\"\n }), \" ensure that the received values have the\\ncorrect type.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"config.cfg\"\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-ini\",\n lang: \"ini\",\n children: \"[nlp.tokenizer]\\n@tokenizers = \\\"bert\_word\_piece\_tokenizer\\\"\\nvocab\_file = \\\"bert-base-uncased-vocab.txt\\\"\\nlowercase = true\\n\"\n })\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"functions.py\",\n highlight: \"1\",\n children: \"@spacy.registry.tokenizers(\\\"bert\_word\_piece\_tokenizer\\\")\\ndef create\_bert\_tokenizer(vocab\_file: str, lowercase: bool):\\n def create\_tokenizer(nlp):\\n return BertTokenizer(nlp.vocab, vocab\_file, lowercase)\\n\\n return create\_tokenizer\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"To avoid hard-coding local paths into your config file, you can also set the\\nvocab path on the CLI by using the \", \_jsx(InlineCode, {\n children: \"--nlp.tokenizer.vocab\_file\"\n }), \"\\n\", \_jsx(\_components.a, {\n href: \"/usage/training#config-overrides\",\n children: \"override\"\n }), \" when you run\\n\", \_jsx(\_components.a, {\n href: \"/api/cli#train\",\n children: \_jsx(InlineCode, {\n children: \"spacy train\"\n })\n }), \". For more details on using registered functions,\\nsee the docs in \", \_jsx(\_components.a, {\n href: \"/usage/training#custom-code\",\n children: \"training with custom code\"\n }), \".\"]\n }), \_jsx(Infobox, {\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"Remember that a registered function should always be a function that spaCy\\n\", \_jsx(\_components.strong, {\n children: \"calls to create something\"\n }), \", not the “something” itself. In this case, it\\n\", \_jsx(\_components.strong, {\n children: \"creates a function\"\n }), \" that takes the \", \_jsx(InlineCode, {\n children: \"nlp\"\n }), \" object and returns a callable that\\ntakes a text and returns a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \".\"]\n })\n }), \_jsx(\_components.h4, {\n id: \"own-annotations\",\n children: \"Using pre-tokenized text \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy generally assumes by default that your data is \", \_jsx(\_components.strong, {\n children: \"raw text\"\n }), \". However,\\nsometimes your data is partially annotated, e.g. with pre-existing tokenization,\\npart-of-speech tags, etc. The most common situation is that you have\\n\", \_jsx(\_components.strong, {\n children: \"pre-defined tokenization\"\n }), \". If you have a list of strings, you can create a\\n\", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object directly. Optionally, you can also specify a list of\\nboolean values, indicating whether each word is followed by a space.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"✏️ Things to try\"\n }), \"\\n\", \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"Change a boolean value in the list of \", \_jsx(InlineCode, {\n children: \"spaces\"\n }), \". You should see it reflected\\nin the \", \_jsx(InlineCode, {\n children: \"doc.text\"\n }), \" and whether the token is followed by a space.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Remove \", \_jsx(InlineCode, {\n children: \"spaces=spaces\"\n }), \" from the \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \". You should see that every token is\\nnow followed by a space.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Copy-paste a random sentence from the internet and manually construct a\\n\", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" with \", \_jsx(InlineCode, {\n children: \"words\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"spaces\"\n }), \" so that the \", \_jsx(InlineCode, {\n children: \"doc.text\"\n }), \" matches the original\\ninput text.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.tokens import Doc\\n\\nnlp = spacy.blank(\\\"en\\\")\\nwords = [\\\"Hello\\\", \\\",\\\", \\\"world\\\", \\\"!\\\"]\\nspaces = [False, True, False, False]\\ndoc = Doc(nlp.vocab, words=words, spaces=spaces)\\nprint(doc.text)\\nprint([(t.text, t.text\_with\_ws, t.whitespace\_) for t in doc])\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"If provided, the spaces list must be the \", \_jsx(\_components.strong, {\n children: \"same length\"\n }), \" as the words list. The\\nspaces list affects the \", \_jsx(InlineCode, {\n children: \"doc.text\"\n }), \", \", \_jsx(InlineCode, {\n children: \"span.text\"\n }), \", \", \_jsx(InlineCode, {\n children: \"token.idx\"\n }), \", \", \_jsx(InlineCode, {\n children: \"span.start\_char\"\n }), \"\\nand \", \_jsx(InlineCode, {\n children: \"span.end\_char\"\n }), \" attributes. If you don’t provide a \", \_jsx(InlineCode, {\n children: \"spaces\"\n }), \" sequence, spaCy\\nwill assume that all words are followed by a space. Once you have a\\n\", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object, you can write to its attributes to set the\\npart-of-speech tags, syntactic dependencies, named entities and other\\nattributes.\"]\n }), \_jsx(\_components.h4, {\n id: \"aligning-tokenization\",\n children: \"Aligning tokenization \"\n }), \_jsxs(\_components.p, {\n children: [\"spaCy’s tokenization is non-destructive and uses language-specific rules\\noptimized for compatibility with treebank annotations. Other tools and resources\\ncan sometimes tokenize things differently – for example, \", \_jsx(InlineCode, {\n children: \"\\\"I'm\\\"\"\n }), \" →\\n\", \_jsx(InlineCode, {\n children: \"[\\\"I\\\", \\\"'\\\", \\\"m\\\"]\"\n }), \" instead of \", \_jsx(InlineCode, {\n children: \"[\\\"I\\\", \\\"'m\\\"]\"\n }), \".\"]\n }), \_jsxs(\_components.p, {\n children: [\"In situations like that, you often want to align the tokenization so that you\\ncan merge annotations from different sources together, or take vectors predicted\\nby a\\n\", \_jsx(\_components.a, {\n href: \"https://github.com/huggingface/pytorch-transformers\",\n children: \"pretrained BERT model\"\n }), \" and\\napply them to spaCy tokens. spaCy’s \", \_jsx(\_components.a, {\n href: \"/api/example#alignment-object\",\n children: \_jsx(InlineCode, {\n children: \"Alignment\"\n })\n }), \"\\nobject allows the one-to-one mappings of token indices in both directions as\\nwell as taking into account indices where multiple tokens align to one single\\ntoken.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"✏️ Things to try\"\n }), \"\\n\", \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"Change the capitalization in one of the token lists – for example,\\n\", \_jsx(InlineCode, {\n children: \"\\\"obama\\\"\"\n }), \" to \", \_jsx(InlineCode, {\n children: \"\\\"Obama\\\"\"\n }), \". You’ll see that the alignment is case-insensitive.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Change \", \_jsx(InlineCode, {\n children: \"\\\"podcasts\\\"\"\n }), \" in \", \_jsx(InlineCode, {\n children: \"other\_tokens\"\n }), \" to \", \_jsx(InlineCode, {\n children: \"\\\"pod\\\", \\\"casts\\\"\"\n }), \". You should see\\nthat there are now two tokens of length 2 in \", \_jsx(InlineCode, {\n children: \"y2x\"\n }), \", one corresponding to\\n“‘s”, and one to “podcasts”.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Make \", \_jsx(InlineCode, {\n children: \"other\_tokens\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"spacy\_tokens\"\n }), \" identical. You’ll see that all\\ntokens now correspond 1-to-1.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"from spacy.training import Alignment\\n\\nother\_tokens = [\\\"i\\\", \\\"listened\\\", \\\"to\\\", \\\"obama\\\", \\\"'\\\", \\\"s\\\", \\\"podcasts\\\", \\\".\\\"]\\nspacy\_tokens = [\\\"i\\\", \\\"listened\\\", \\\"to\\\", \\\"obama\\\", \\\"'s\\\", \\\"podcasts\\\", \\\".\\\"]\\nalign = Alignment.from\_strings(other\_tokens, spacy\_tokens)\\nprint(f\\\"a -\u003e b, lengths: {align.x2y.lengths}\\\") # array([1, 1, 1, 1, 1, 1, 1, 1])\\nprint(f\\\"a -\u003e b, mapping: {align.x2y.data}\\\") # array([0, 1, 2, 3, 4, 4, 5, 6]) : two tokens both refer to \\\"'s\\\"\\nprint(f\\\"b -\u003e a, lengths: {align.y2x.lengths}\\\") # array([1, 1, 1, 1, 2, 1, 1]) : the token \\\"'s\\\" refers to two tokens\\nprint(f\\\"b -\u003e a, mappings: {align.y2x.data}\\\") # array([0, 1, 2, 3, 4, 5, 6, 7])\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"Here are some insights from the alignment information generated in the example\\nabove:\"\n }), \_jsxs(\_components.ul, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"The one-to-one mappings for the first four tokens are identical, which means\\nthey map to each other. This makes sense because they’re also identical in the\\ninput: \", \_jsx(InlineCode, {\n children: \"\\\"i\\\"\"\n }), \", \", \_jsx(InlineCode, {\n children: \"\\\"listened\\\"\"\n }), \", \", \_jsx(InlineCode, {\n children: \"\\\"to\\\"\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"\\\"obama\\\"\"\n }), \".\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"The value of \", \_jsx(InlineCode, {\n children: \"x2y.data[6]\"\n }), \" is \", \_jsx(InlineCode, {\n children: \"5\"\n }), \", which means that \", \_jsx(InlineCode, {\n children: \"other\_tokens[6]\"\n }), \"\\n(\", \_jsx(InlineCode, {\n children: \"\\\"podcasts\\\"\"\n }), \") aligns to \", \_jsx(InlineCode, {\n children: \"spacy\_tokens[5]\"\n }), \" (also \", \_jsx(InlineCode, {\n children: \"\\\"podcasts\\\"\"\n }), \").\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(InlineCode, {\n children: \"x2y.data[4]\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"x2y.data[5]\"\n }), \" are both \", \_jsx(InlineCode, {\n children: \"4\"\n }), \", which means that both tokens 4\\nand 5 of \", \_jsx(InlineCode, {\n children: \"other\_tokens\"\n }), \" (\", \_jsx(InlineCode, {\n children: \"\\\"'\\\"\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"\\\"s\\\"\"\n }), \") align to token 4 of \", \_jsx(InlineCode, {\n children: \"spacy\_tokens\"\n }), \"\\n(\", \_jsx(InlineCode, {\n children: \"\\\"'s\\\"\"\n }), \").\"]\n }), \"\\n\"]\n }), \_jsx(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"The current implementation of the alignment algorithm assumes that both\\ntokenizations add up to the same string. For example, you’ll be able to align\\n\", \_jsx(InlineCode, {\n children: \"[\\\"I\\\", \\\"'\\\", \\\"m\\\"]\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"[\\\"I\\\", \\\"'m\\\"]\"\n }), \", which both add up to \", \_jsx(InlineCode, {\n children: \"\\\"I'm\\\"\"\n }), \", but not\\n\", \_jsx(InlineCode, {\n children: \"[\\\"I\\\", \\\"'m\\\"]\"\n }), \" and \", \_jsx(InlineCode, {\n children: \"[\\\"I\\\", \\\"am\\\"]\"\n }), \".\"]\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-retokenization\",\n children: [\_jsx(\_components.h2, {\n id: \"retokenization\",\n version: \"2.1\",\n children: \"Merging and splitting \"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/doc#retokenize\",\n children: \_jsx(InlineCode, {\n children: \"Doc.retokenize\"\n })\n }), \" context manager lets you merge and\\nsplit tokens. Modifications to the tokenization are stored and performed all at\\nonce when the context manager exits. To merge several tokens into one single\\ntoken, pass a \", \_jsx(InlineCode, {\n children: \"Span\"\n }), \" to \", \_jsx(\_components.a, {\n href: \"/api/doc#retokenizer.merge\",\n children: \_jsx(InlineCode, {\n children: \"retokenizer.merge\"\n })\n }), \". An\\noptional dictionary of \", \_jsx(InlineCode, {\n children: \"attrs\"\n }), \" lets you set attributes that will be assigned to\\nthe merged token – for example, the lemma, part-of-speech tag or entity type. By\\ndefault, the merged token will receive the same attributes as the merged span’s\\nroot.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"✏️ Things to try\"\n }), \"\\n\", \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"Inspect the \", \_jsx(InlineCode, {\n children: \"token.lemma\_\"\n }), \" attribute with and without setting the \", \_jsx(InlineCode, {\n children: \"attrs\"\n }), \".\\nYou’ll see that the lemma defaults to “New”, the lemma of the span’s root.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Overwrite other attributes like the \", \_jsx(InlineCode, {\n children: \"\\\"ENT\_TYPE\\\"\"\n }), \". Since “New York” is also\\nrecognized as a named entity, this change will also be reflected in the\\n\", \_jsx(InlineCode, {\n children: \"doc.ents\"\n }), \".\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"I live in New York\\\")\\nprint(\\\"Before:\\\", [token.text for token in doc])\\n\\nwith doc.retokenize() as retokenizer:\\n retokenizer.merge(doc[3:5], attrs={\\\"LEMMA\\\": \\\"new york\\\"})\\nprint(\\\"After:\\\", [token.text for token in doc])\\n\"\n })\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Tip: merging entities and noun phrases\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"If you need to merge named entities or noun chunks, check out the built-in\\n\", \_jsx(\_components.a, {\n href: \"/api/pipeline-functions#merge\_entities\",\n children: \_jsx(InlineCode, {\n children: \"merge\_entities\"\n })\n }), \" and\\n\", \_jsx(\_components.a, {\n href: \"/api/pipeline-functions#merge\_noun\_chunks\",\n children: \_jsx(InlineCode, {\n children: \"merge\_noun\_chunks\"\n })\n }), \" pipeline\\ncomponents. When added to your pipeline using \", \_jsx(InlineCode, {\n children: \"nlp.add\_pipe\"\n }), \", they’ll take\\ncare of merging the spans automatically.\"]\n }), \"\\n\"]\n }), \_jsxs(\_components.p, {\n children: [\"If an attribute in the \", \_jsx(InlineCode, {\n children: \"attrs\"\n }), \" is a context-dependent token attribute, it will\\nbe applied to the underlying \", \_jsx(\_components.a, {\n href: \"/api/token\",\n children: \_jsx(InlineCode, {\n children: \"Token\"\n })\n }), \". For example \", \_jsx(InlineCode, {\n children: \"LEMMA\"\n }), \", \", \_jsx(InlineCode, {\n children: \"POS\"\n }), \"\\nor \", \_jsx(InlineCode, {\n children: \"DEP\"\n }), \" only apply to a word in context, so they’re token attributes. If an\\nattribute is a context-independent lexical attribute, it will be applied to the\\nunderlying \", \_jsx(\_components.a, {\n href: \"/api/lexeme\",\n children: \_jsx(InlineCode, {\n children: \"Lexeme\"\n })\n }), \", the entry in the vocabulary. For example,\\n\", \_jsx(InlineCode, {\n children: \"LOWER\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"IS\_STOP\"\n }), \" apply to all words of the same spelling, regardless of the\\ncontext.\"]\n }), \_jsxs(Infobox, {\n variant: \"warning\",\n title: \"Note on merging overlapping spans\",\n children: [\_jsxs(\_components.p, {\n children: [\"If you’re trying to merge spans that overlap, spaCy will raise an error because\\nit’s unclear how the result should look. Depending on the application, you may\\nwant to match the shortest or longest possible span, so it’s up to you to filter\\nthem. If you’re looking for the longest non-overlapping span, you can use the\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#util.filter\_spans\",\n children: \_jsx(InlineCode, {\n children: \"util.filter\_spans\"\n })\n }), \" helper:\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"doc = nlp(\\\"I live in Berlin Kreuzberg\\\")\\nspans = [doc[3:5], doc[3:4], doc[4:5]]\\nfiltered\_spans = filter\_spans(spans)\\n\"\n })\n })]\n }), \_jsx(\_components.h3, {\n children: \"Splitting tokens\"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/doc#retokenizer.split\",\n children: \_jsx(InlineCode, {\n children: \"retokenizer.split\"\n })\n }), \" method allows splitting\\none token into two or more tokens. This can be useful for cases where\\ntokenization rules alone aren’t sufficient. For example, you might want to split\\n“its” into the tokens “it” and “is” – but not the possessive pronoun “its”. You\\ncan write rule-based logic that can find only the correct “its” to split, but by\\nthat time, the \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" will already be tokenized.\"]\n }), \_jsxs(\_components.p, {\n children: [\"This process of splitting a token requires more settings, because you need to\\nspecify the text of the individual tokens, optional per-token attributes and how\\nthe tokens should be attached to the existing syntax tree. This can be done by\\nsupplying a list of \", \_jsx(InlineCode, {\n children: \"heads\"\n }), \" – either the token to attach the newly split token\\nto, or a \", \_jsx(InlineCode, {\n children: \"(token, subtoken)\"\n }), \" tuple if the newly split token should be attached\\nto another subtoken. In this case, “New” should be attached to “York” (the\\nsecond split subtoken) and “York” should be attached to “in”.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"✏️ Things to try\"\n }), \"\\n\", \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsx(\_components.li, {\n children: \"Assign different attributes to the subtokens and compare the result.\"\n }), \"\\n\", \_jsx(\_components.li, {\n children: \"Change the heads so that “New” is attached to “in” and “York” is attached\\nto “New”.\"\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Split the token into three tokens instead of two – for example,\\n\", \_jsx(InlineCode, {\n children: \"[\\\"New\\\", \\\"Yo\\\", \\\"rk\\\"]\"\n }), \".\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy import displacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"I live in NewYork\\\")\\nprint(\\\"Before:\\\", [token.text for token in doc])\\ndisplacy.render(doc) # displacy.serve if you're not in a Jupyter environment\\n\\nwith doc.retokenize() as retokenizer:\\n heads = [(doc[3], 1), doc[2]]\\n attrs = {\\\"POS\\\": [\\\"PROPN\\\", \\\"PROPN\\\"], \\\"DEP\\\": [\\\"pobj\\\", \\\"compound\\\"]}\\n retokenizer.split(doc[3], [\\\"New\\\", \\\"York\\\"], heads=heads, attrs=attrs)\\nprint(\\\"After:\\\", [token.text for token in doc])\\ndisplacy.render(doc) # displacy.serve if you're not in a Jupyter environment\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"Specifying the heads as a list of \", \_jsx(InlineCode, {\n children: \"token\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"(token, subtoken)\"\n }), \" tuples allows\\nattaching split subtokens to other subtokens, without having to keep track of\\nthe token indices after splitting.\"]\n }), \_jsxs(\_components.table, {\n children: [\_jsx(\_components.thead, {\n children: \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.th, {\n children: \"Token\"\n }), \_jsx(\_components.th, {\n children: \"Head\"\n }), \_jsx(\_components.th, {\n children: \"Description\"\n })]\n })\n }), \_jsxs(\_components.tbody, {\n children: [\_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"New\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"(doc[3], 1)\"\n })\n }), \_jsxs(\_components.td, {\n children: [\"Attach this token to the second subtoken (index \", \_jsx(InlineCode, {\n children: \"1\"\n }), \") that \", \_jsx(InlineCode, {\n children: \"doc[3]\"\n }), \" will be split into, i.e. “York”.\"]\n })]\n }), \_jsxs(\_components.tr, {\n children: [\_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"\\\"York\\\"\"\n })\n }), \_jsx(\_components.td, {\n children: \_jsx(InlineCode, {\n children: \"doc[2]\"\n })\n }), \_jsxs(\_components.td, {\n children: [\"Attach this token to \", \_jsx(InlineCode, {\n children: \"doc[1]\"\n }), \" in the original \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \", i.e. “in”.\"]\n })]\n })]\n })]\n }), \_jsx(\_components.p, {\n children: \"If you don’t care about the heads (for example, if you’re only running the\\ntokenizer and not the parser), you can attach each subtoken to itself:\"\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n highlight: \"3\",\n children: \"doc = nlp(\\\"I live in NewYorkCity\\\")\\nwith doc.retokenize() as retokenizer:\\n heads = [(doc[3], 0), (doc[3], 1), (doc[3], 2)]\\n retokenizer.split(doc[3], [\\\"New\\\", \\\"York\\\", \\\"City\\\"], heads=heads)\\n\"\n })\n }), \_jsxs(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: [\_jsxs(\_components.p, {\n children: [\"When splitting tokens, the subtoken texts always have to match the original\\ntoken text – or, put differently \", \_jsx(InlineCode, {\n children: \"\\\"\\\".join(subtokens) == token.text\"\n }), \" always needs\\nto hold true. If this wasn’t the case, splitting tokens could easily end up\\nproducing confusing and unexpected results that would contradict spaCy’s\\nnon-destructive tokenization policy.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-diff\",\n lang: \"diff\",\n children: \"doc = nlp(\\\"I live in L.A.\\\")\\nwith doc.retokenize() as retokenizer:\\n- retokenizer.split(doc[3], [\\\"Los\\\", \\\"Angeles\\\"], heads=[(doc[3], 1), doc[2]])\\n+ retokenizer.split(doc[3], [\\\"L.\\\", \\\"A.\\\"], heads=[(doc[3], 1), doc[2]])\\n\"\n })\n })]\n }), \_jsx(\_components.h3, {\n id: \"retokenization-extensions\",\n children: \"Overwriting custom extension attributes \"\n }), \_jsxs(\_components.p, {\n children: [\"If you’ve registered custom\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines#custom-components-attributes\",\n children: \"extension attributes\"\n }), \",\\nyou can overwrite them during tokenization by providing a dictionary of\\nattribute names mapped to new values as the \", \_jsx(InlineCode, {\n children: \"\\\"\_\\\"\"\n }), \" key in the \", \_jsx(InlineCode, {\n children: \"attrs\"\n }), \". For\\nmerging, you need to provide one dictionary of attributes for the resulting\\nmerged token. For splitting, you need to provide a list of dictionaries with\\ncustom attributes, one per split subtoken.\"]\n }), \_jsx(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"To set extension attributes during retokenization, the attributes need to be\\n\", \_jsx(\_components.strong, {\n children: \"registered\"\n }), \" using the \", \_jsx(\_components.a, {\n href: \"/api/token#set\_extension\",\n children: \_jsx(InlineCode, {\n children: \"Token.set\_extension\"\n })\n }), \"\\nmethod and they need to be \", \_jsx(\_components.strong, {\n children: \"writable\"\n }), \". This means that they should either have\\na default value that can be overwritten, or a getter \", \_jsx(\_components.em, {\n children: \"and\"\n }), \" setter. Method\\nextensions or extensions with only a getter are computed dynamically, so their\\nvalues can’t be overwritten. For more details, see the\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines/#custom-components-attributes\",\n children: \"extension attribute docs\"\n }), \".\"]\n })\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"✏️ Things to try\"\n }), \"\\n\", \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"Add another custom extension – maybe \", \_jsx(InlineCode, {\n children: \"\\\"music\_style\\\"\"\n }), \"? – and overwrite it.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Change the extension attribute to use only a \", \_jsx(InlineCode, {\n children: \"getter\"\n }), \" function. You should\\nsee that spaCy raises an error, because the attribute is not writable\\nanymore.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Rewrite the code to split a token with \", \_jsx(InlineCode, {\n children: \"retokenizer.split\"\n }), \". Remember that\\nyou need to provide a list of extension attribute values as the \", \_jsx(InlineCode, {\n children: \"\\\"\_\\\"\"\n }), \"\\nproperty, one for each split subtoken.\"]\n }), \"\\n\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.tokens import Token\\n\\n# Register a custom token attribute, token.\_.is\_musician\\nToken.set\_extension(\\\"is\_musician\\\", default=False)\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"I like David Bowie\\\")\\nprint(\\\"Before:\\\", [(token.text, token.\_.is\_musician) for token in doc])\\n\\nwith doc.retokenize() as retokenizer:\\n retokenizer.merge(doc[2:4], attrs={\\\"\_\\\": {\\\"is\_musician\\\": True}})\\nprint(\\\"After:\\\", [(token.text, token.\_.is\_musician) for token in doc])\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-sbd\",\n children: [\_jsx(\_components.h2, {\n id: \"sbd\",\n children: \"Sentence Segmentation \"\n }), \_jsxs(\_components.p, {\n children: [\"A \", \_jsx(\_components.a, {\n href: \"/api/doc\",\n children: \_jsx(InlineCode, {\n children: \"Doc\"\n })\n }), \" object’s sentences are available via the \", \_jsx(InlineCode, {\n children: \"Doc.sents\"\n }), \"\\nproperty. To view a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \"’s sentences, you can iterate over the \", \_jsx(InlineCode, {\n children: \"Doc.sents\"\n }), \", a\\ngenerator that yields \", \_jsx(\_components.a, {\n href: \"/api/span\",\n children: \_jsx(InlineCode, {\n children: \"Span\"\n })\n }), \" objects. You can check whether a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \"\\nhas sentence boundaries by calling\\n\", \_jsx(\_components.a, {\n href: \"/api/doc#has\_annotation\",\n children: \_jsx(InlineCode, {\n children: \"Doc.has\_annotation\"\n })\n }), \" with the attribute name\\n\", \_jsx(InlineCode, {\n children: \"\\\"SENT\_START\\\"\"\n }), \".\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"This is a sentence. This is another sentence.\\\")\\nassert doc.has\_annotation(\\\"SENT\_START\\\")\\nfor sent in doc.sents:\\n print(sent.text)\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"spaCy provides four alternatives for sentence segmentation:\"\n }), \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.a, {\n href: \"#sbd-parser\",\n children: \"Dependency parser\"\n }), \": the statistical\\n\", \_jsx(\_components.a, {\n href: \"/api/dependencyparser\",\n children: \_jsx(InlineCode, {\n children: \"DependencyParser\"\n })\n }), \" provides the most accurate\\nsentence boundaries based on full dependency parses.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.a, {\n href: \"#sbd-senter\",\n children: \"Statistical sentence segmenter\"\n }), \": the statistical\\n\", \_jsx(\_components.a, {\n href: \"/api/sentencerecognizer\",\n children: \_jsx(InlineCode, {\n children: \"SentenceRecognizer\"\n })\n }), \" is a simpler and faster\\nalternative to the parser that only sets sentence boundaries.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.a, {\n href: \"#sbd-component\",\n children: \"Rule-based pipeline component\"\n }), \": the rule-based\\n\", \_jsx(\_components.a, {\n href: \"/api/sentencizer\",\n children: \_jsx(InlineCode, {\n children: \"Sentencizer\"\n })\n }), \" sets sentence boundaries using a\\ncustomizable list of sentence-final punctuation.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\_jsx(\_components.a, {\n href: \"#sbd-custom\",\n children: \"Custom function\"\n }), \": your own custom function added to the\\nprocessing pipeline can set sentence boundaries by writing to\\n\", \_jsx(InlineCode, {\n children: \"Token.is\_sent\_start\"\n }), \".\"]\n }), \"\\n\"]\n }), \_jsx(\_components.h3, {\n id: \"sbd-parser\",\n model: \"parser\",\n children: \"Default: Using the dependency parse \"\n }), \_jsxs(\_components.p, {\n children: [\"Unlike other libraries, spaCy uses the dependency parse to determine sentence\\nboundaries. This is usually the most accurate approach, but it requires a\\n\", \_jsx(\_components.strong, {\n children: \"trained pipeline\"\n }), \" that provides accurate predictions. If your texts are\\ncloser to general-purpose news or web text, this should work well out-of-the-box\\nwith spaCy’s provided trained pipelines. For social media or conversational text\\nthat doesn’t follow the same rules, your application may benefit from a custom\\ntrained or rule-based component.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(\\\"This is a sentence. This is another sentence.\\\")\\nfor sent in doc.sents:\\n print(sent.text)\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"spaCy’s dependency parser respects already set boundaries, so you can preprocess\\nyour \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" using custom components \", \_jsx(\_components.em, {\n children: \"before\"\n }), \" it’s parsed. Depending on your text,\\nthis may also improve parse accuracy, since the parser is constrained to predict\\nparses consistent with the sentence boundaries.\"]\n }), \_jsx(\_components.h3, {\n id: \"sbd-senter\",\n model: \"senter\",\n version: \"3\",\n children: \"Statistical sentence segmenter \"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/sentencerecognizer\",\n children: \_jsx(InlineCode, {\n children: \"SentenceRecognizer\"\n })\n }), \" is a simple statistical\\ncomponent that only provides sentence boundaries. Along with being faster and\\nsmaller than the parser, its primary advantage is that it’s easier to train\\nbecause it only requires annotated sentence boundaries rather than full\\ndependency parses. spaCy’s \", \_jsx(\_components.a, {\n href: \"/models\",\n children: \"trained pipelines\"\n }), \" include both a parser\\nand a trained sentence segmenter, which is\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines#disabling\",\n children: \"disabled\"\n }), \" by default. If you only need\\nsentence boundaries and no parser, you can use the \", \_jsx(InlineCode, {\n children: \"exclude\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"disable\"\n }), \"\\nargument on \", \_jsx(\_components.a, {\n href: \"/api/top-level#spacy.load\",\n children: \_jsx(InlineCode, {\n children: \"spacy.load\"\n })\n }), \" to load the pipeline\\nwithout the parser and then enable the sentence recognizer explicitly with\\n\", \_jsx(\_components.a, {\n href: \"/api/language#enable\_pipe\",\n children: \_jsx(InlineCode, {\n children: \"nlp.enable\_pipe\"\n })\n }), \".\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"senter vs. parser\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"The recall for the \", \_jsx(InlineCode, {\n children: \"senter\"\n }), \" is typically slightly lower than for the parser,\\nwhich is better at predicting sentence boundaries when punctuation is not\\npresent.\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\", exclude=[\\\"parser\\\"])\\nnlp.enable\_pipe(\\\"senter\\\")\\ndoc = nlp(\\\"This is a sentence. This is another sentence.\\\")\\nfor sent in doc.sents:\\n print(sent.text)\\n\"\n })\n }), \_jsx(\_components.h3, {\n id: \"sbd-component\",\n children: \"Rule-based pipeline component \"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/sentencizer\",\n children: \_jsx(InlineCode, {\n children: \"Sentencizer\"\n })\n }), \" component is a\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines\",\n children: \"pipeline component\"\n }), \" that splits sentences on\\npunctuation like \", \_jsx(InlineCode, {\n children: \".\"\n }), \", \", \_jsx(InlineCode, {\n children: \"!\"\n }), \" or \", \_jsx(InlineCode, {\n children: \"?\"\n }), \". You can plug it into your pipeline if you only\\nneed sentence boundaries without dependency parses.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\nfrom spacy.lang.en import English\\n\\nnlp = English() # just the language with no pipeline\\nnlp.add\_pipe(\\\"sentencizer\\\")\\ndoc = nlp(\\\"This is a sentence. This is another sentence.\\\")\\nfor sent in doc.sents:\\n print(sent.text)\\n\"\n })\n }), \_jsx(\_components.h3, {\n id: \"sbd-custom\",\n children: \"Custom rule-based strategy \"\n }), \_jsxs(\_components.p, {\n children: [\"If you want to implement your own strategy that differs from the default\\nrule-based approach of splitting on sentences, you can also create a\\n\", \_jsx(\_components.a, {\n href: \"/usage/processing-pipelines#custom-components\",\n children: \"custom pipeline component\"\n }), \" that\\ntakes a \", \_jsx(InlineCode, {\n children: \"Doc\"\n }), \" object and sets the \", \_jsx(InlineCode, {\n children: \"Token.is\_sent\_start\"\n }), \" attribute on each\\nindividual token. If set to \", \_jsx(InlineCode, {\n children: \"False\"\n }), \", the token is explicitly marked as \", \_jsx(\_components.em, {\n children: \"not\"\n }), \" the\\nstart of a sentence. If set to \", \_jsx(InlineCode, {\n children: \"None\"\n }), \" (default), it’s treated as a missing value\\nand can still be overwritten by the parser.\"]\n }), \_jsx(Infobox, {\n title: \"Important note\",\n variant: \"warning\",\n children: \_jsxs(\_components.p, {\n children: [\"To prevent inconsistent state, you can only set boundaries \", \_jsx(\_components.strong, {\n children: \"before\"\n }), \" a document\\nis parsed (and \", \_jsx(InlineCode, {\n children: \"doc.has\_annotation(\\\"DEP\\\")\"\n }), \" is \", \_jsx(InlineCode, {\n children: \"False\"\n }), \"). To ensure that your\\ncomponent is added in the right place, you can set \", \_jsx(InlineCode, {\n children: \"before='parser'\"\n }), \" or\\n\", \_jsx(InlineCode, {\n children: \"first=True\"\n }), \" when adding it to the pipeline using\\n\", \_jsx(\_components.a, {\n href: \"/api/language#add\_pipe\",\n children: \_jsx(InlineCode, {\n children: \"nlp.add\_pipe\"\n })\n }), \".\"]\n })\n }), \_jsxs(\_components.p, {\n children: [\"Here’s an example of a component that implements a pre-processing rule for\\nsplitting on \", \_jsx(InlineCode, {\n children: \"\\\"...\\\"\"\n }), \" tokens. The component is added before the parser, which is\\nthen used to further segment the text. That’s possible, because \", \_jsx(InlineCode, {\n children: \"is\_sent\_start\"\n }), \"\\nis only set to \", \_jsx(InlineCode, {\n children: \"True\"\n }), \" for some of the tokens – all others still specify \", \_jsx(InlineCode, {\n children: \"None\"\n }), \"\\nfor unset sentence boundaries. This approach can be useful if you want to\\nimplement \", \_jsx(\_components.strong, {\n children: \"additional\"\n }), \" rules specific to your data, while still being able to\\ntake advantage of dependency-based sentence segmentation.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"from spacy.language import Language\\nimport spacy\\n\\ntext = \\\"this is a sentence...hello...and another sentence.\\\"\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ndoc = nlp(text)\\nprint(\\\"Before:\\\", [sent.text for sent in doc.sents])\\n\\n@Language.component(\\\"set\_custom\_boundaries\\\")\\ndef set\_custom\_boundaries(doc):\\n for token in doc[:-1]:\\n if token.text == \\\"...\\\":\\n doc[token.i + 1].is\_sent\_start = True\\n return doc\\n\\nnlp.add\_pipe(\\\"set\_custom\_boundaries\\\", before=\\\"parser\\\")\\ndoc = nlp(text)\\nprint(\\\"After:\\\", [sent.text for sent in doc.sents])\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-mappings-exceptions\",\n children: [\_jsx(\_components.h2, {\n id: \"mappings-exceptions\",\n version: \"3\",\n children: \"Mappings \u0026 Exceptions \"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/attributeruler\",\n children: \_jsx(InlineCode, {\n children: \"AttributeRuler\"\n })\n }), \" manages \", \_jsx(\_components.strong, {\n children: \"rule-based mappings and\\nexceptions\"\n }), \" for all token-level attributes. As the number of\\n\", \_jsx(\_components.a, {\n href: \"/api/#architecture-pipeline\",\n children: \"pipeline components\"\n }), \" has grown from spaCy v2 to\\nv3, handling rules and exceptions in each component individually has become\\nimpractical, so the \", \_jsx(InlineCode, {\n children: \"AttributeRuler\"\n }), \" provides a single component with a unified\\npattern format for all token attribute mappings and exceptions.\"]\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(InlineCode, {\n children: \"AttributeRuler\"\n }), \" uses\\n\", \_jsxs(\_components.a, {\n href: \"/usage/rule-based-matching#adding-patterns\",\n children: [\_jsx(InlineCode, {\n children: \"Matcher\"\n }), \" patterns\"]\n }), \" to identify\\ntokens and then assigns them the provided attributes. If needed, the\\n\", \_jsx(\_components.a, {\n href: \"/api/matcher\",\n children: \_jsx(InlineCode, {\n children: \"Matcher\"\n })\n }), \" patterns can include context around the target token.\\nFor example, the attribute ruler can:\"]\n }), \_jsxs(\_components.ul, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"provide exceptions for any \", \_jsx(\_components.strong, {\n children: \"token attributes\"\n })]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"map \", \_jsx(\_components.strong, {\n children: \"fine-grained tags\"\n }), \" to \", \_jsx(\_components.strong, {\n children: \"coarse-grained tags\"\n }), \" for languages without\\nstatistical morphologizers (replacing the v2.x \", \_jsx(InlineCode, {\n children: \"tag\_map\"\n }), \" in the\\n\", \_jsx(\_components.a, {\n href: \"#language-data\",\n children: \"language data\"\n }), \")\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"map token \", \_jsx(\_components.strong, {\n children: \"surface form + fine-grained tags\"\n }), \" to \", \_jsx(\_components.strong, {\n children: \"morphological features\"\n }), \"\\n(replacing the v2.x \", \_jsx(InlineCode, {\n children: \"morph\_rules\"\n }), \" in the \", \_jsx(\_components.a, {\n href: \"#language-data\",\n children: \"language data\"\n }), \")\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"specify the \", \_jsx(\_components.strong, {\n children: \"tags for space tokens\"\n }), \" (replacing hard-coded behavior in the\\ntagger)\"]\n }), \"\\n\"]\n }), \_jsxs(\_components.p, {\n children: [\"The following example shows how the tag and POS \", \_jsx(InlineCode, {\n children: \"NNP\"\n }), \"/\", \_jsx(InlineCode, {\n children: \"PROPN\"\n }), \" can be specified\\nfor the phrase \", \_jsx(InlineCode, {\n children: \"\\\"The Who\\\"\"\n }), \", overriding the tags provided by the statistical\\ntagger and the POS tag map.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"import spacy\\n\\nnlp = spacy.load(\\\"en\_core\_web\_sm\\\")\\ntext = \\\"I saw The Who perform. Who did you see?\\\"\\ndoc1 = nlp(text)\\nprint(doc1[2].tag\_, doc1[2].pos\_) # DT DET\\nprint(doc1[3].tag\_, doc1[3].pos\_) # WP PRON\\n\\n# Add attribute ruler with exception for \\\"The Who\\\" as NNP/PROPN NNP/PROPN\\nruler = nlp.get\_pipe(\\\"attribute\_ruler\\\")\\n# Pattern to match \\\"The Who\\\"\\npatterns = [[{\\\"LOWER\\\": \\\"the\\\"}, {\\\"TEXT\\\": \\\"Who\\\"}]]\\n# The attributes to assign to the matched token\\nattrs = {\\\"TAG\\\": \\\"NNP\\\", \\\"POS\\\": \\\"PROPN\\\"}\\n# Add rules to the attribute ruler\\nruler.add(patterns=patterns, attrs=attrs, index=0) # \\\"The\\\" in \\\"The Who\\\"\\nruler.add(patterns=patterns, attrs=attrs, index=1) # \\\"Who\\\" in \\\"The Who\\\"\\n\\ndoc2 = nlp(text)\\nprint(doc2[2].tag\_, doc2[2].pos\_) # NNP PROPN\\nprint(doc2[3].tag\_, doc2[3].pos\_) # NNP PROPN\\n# The second \\\"Who\\\" remains unmodified\\nprint(doc2[5].tag\_, doc2[5].pos\_) # WP PRON\\n\"\n })\n }), \_jsx(Infobox, {\n variant: \"warning\",\n title: \"Migrating from spaCy v2.x\",\n children: \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/attributeruler\",\n children: \_jsx(InlineCode, {\n children: \"AttributeRuler\"\n })\n }), \" can import a \", \_jsx(\_components.strong, {\n children: \"tag map and morph\\nrules\"\n }), \" in the v2.x format via its built-in methods or when the component is\\ninitialized before training. See the\\n\", \_jsx(\_components.a, {\n href: \"/usage/v3#migrating-training-mappings-exceptions\",\n children: \"migration guide\"\n }), \" for details.\"]\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-vectors-similarity\",\n children: [\_jsx(\_components.h2, {\n id: \"vectors-similarity\",\n children: \"Word vectors and semantic similarity \"\n }), \_jsx(Vectors101, {}), \_jsx(\_components.h3, {\n id: \"adding-vectors\",\n children: \"Adding word vectors \"\n }), \_jsxs(\_components.p, {\n children: [\"Custom word vectors can be trained using a number of open-source libraries, such\\nas \", \_jsx(\_components.a, {\n href: \"https://radimrehurek.com/gensim\",\n children: \"Gensim\"\n }), \", \", \_jsx(\_components.a, {\n href: \"https://fasttext.cc\",\n children: \"FastText\"\n }), \",\\nor Tomas Mikolov’s original\\n\", \_jsx(\_components.a, {\n href: \"https://code.google.com/archive/p/word2vec/\",\n children: \"Word2vec implementation\"\n }), \". Most\\nword vector libraries output an easy-to-read text-based format, where each line\\nconsists of the word followed by its vector. For everyday use, we want to\\nconvert the vectors into a binary format that loads faster and takes up less\\nspace on disk. The easiest way to do this is the\\n\", \_jsx(\_components.a, {\n href: \"/api/cli#init-vectors\",\n children: \_jsx(InlineCode, {\n children: \"init vectors\"\n })\n }), \" command-line utility. This will output a\\nblank spaCy pipeline in the directory \", \_jsx(InlineCode, {\n children: \"/tmp/la\_vectors\_wiki\_lg\"\n }), \", giving you\\naccess to some nice Latin vectors. You can then pass the directory path to\\n\", \_jsx(\_components.a, {\n href: \"/api/top-level#spacy.load\",\n children: \_jsx(InlineCode, {\n children: \"spacy.load\"\n })\n }), \" or use it in the\\n\", \_jsx(\_components.a, {\n href: \"/api/data-formats#config-initialize\",\n children: \_jsx(InlineCode, {\n children: \"[initialize]\"\n })\n }), \" of your config when you\\n\", \_jsx(\_components.a, {\n href: \"/usage/training\",\n children: \"train\"\n }), \" a model.\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Usage example\"\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"nlp\_latin = spacy.load(\\\"/tmp/la\_vectors\_wiki\_lg\\\")\\ndoc1 = nlp\_latin(\\\"Caecilius est in horto\\\")\\ndoc2 = nlp\_latin(\\\"servus est in atrio\\\")\\ndoc1.similarity(doc2)\\n\"\n })\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-bash\",\n lang: \"bash\",\n children: \"$ wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.la.300.vec.gz\\n$ python -m spacy init vectors en cc.la.300.vec.gz /tmp/la\_vectors\_wiki\_lg\\n\"\n })\n }), \_jsxs(Accordion, {\n title: \"How to optimize vector coverage\",\n id: \"custom-vectors-coverage\",\n spaced: true,\n children: [\_jsxs(\_components.p, {\n children: [\"To help you strike a good balance between coverage and memory usage, spaCy’s\\n\", \_jsx(\_components.a, {\n href: \"/api/vectors\",\n children: \_jsx(InlineCode, {\n children: \"Vectors\"\n })\n }), \" class lets you map \", \_jsx(\_components.strong, {\n children: \"multiple keys\"\n }), \" to the \", \_jsx(\_components.strong, {\n children: \"same\\nrow\"\n }), \" of the table. If you’re using the\\n\", \_jsx(\_components.a, {\n href: \"/api/cli#init-vectors\",\n children: \_jsx(InlineCode, {\n children: \"spacy init vectors\"\n })\n }), \" command to create a vocabulary,\\npruning the vectors will be taken care of automatically if you set the \", \_jsx(InlineCode, {\n children: \"--prune\"\n }), \"\\nflag. You can also do it manually in the following steps:\"]\n }), \_jsxs(\_components.ol, {\n children: [\"\\n\", \_jsxs(\_components.li, {\n children: [\"Start with a \", \_jsx(\_components.strong, {\n children: \"word vectors package\"\n }), \" that covers a huge vocabulary. For\\ninstance, the \", \_jsx(\_components.a, {\n href: \"/models/en#en\_core\_web\_lg\",\n children: \_jsx(InlineCode, {\n children: \"en\_core\_web\_lg\"\n })\n }), \" package provides\\n300-dimensional GloVe vectors for 685k terms of English.\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"If your vocabulary has values set for the \", \_jsx(InlineCode, {\n children: \"Lexeme.prob\"\n }), \" attribute, the\\nlexemes will be sorted by descending probability to determine which vectors\\nto prune. Otherwise, lexemes will be sorted by their order in the \", \_jsx(InlineCode, {\n children: \"Vocab\"\n }), \".\"]\n }), \"\\n\", \_jsxs(\_components.li, {\n children: [\"Call \", \_jsx(\_components.a, {\n href: \"/api/vocab#prune\_vectors\",\n children: \_jsx(InlineCode, {\n children: \"Vocab.prune\_vectors\"\n })\n }), \" with the number of\\nvectors you want to keep.\"]\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n children: \"nlp = spacy.load(\\\"en\_core\_web\_lg\\\")\\nn\_vectors = 105000 # number of vectors to keep\\nremoved\_words = nlp.vocab.prune\_vectors(n\_vectors)\\n\\nassert len(nlp.vocab.vectors) \u003c= n\_vectors # unique vectors have been pruned\\nassert nlp.vocab.vectors.n\_keys \u003e n\_vectors # but not the total entries\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\_jsx(\_components.a, {\n href: \"/api/vocab#prune\_vectors\",\n children: \_jsx(InlineCode, {\n children: \"Vocab.prune\_vectors\"\n })\n }), \" reduces the current vector\\ntable to a given number of unique entries, and returns a dictionary containing\\nthe removed words, mapped to \", \_jsx(InlineCode, {\n children: \"(string, score)\"\n }), \" tuples, where \", \_jsx(InlineCode, {\n children: \"string\"\n }), \" is the\\nentry the removed word was mapped to and \", \_jsx(InlineCode, {\n children: \"score\"\n }), \" the similarity score between\\nthe two words.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"Removed words\",\n children: \"{\\n \\\"Shore\\\": (\\\"coast\\\", 0.732257),\\n \\\"Precautionary\\\": (\\\"caution\\\", 0.490973),\\n \\\"hopelessness\\\": (\\\"sadness\\\", 0.742366),\\n \\\"Continuous\\\": (\\\"continuous\\\", 0.732549),\\n \\\"Disemboweled\\\": (\\\"corpse\\\", 0.499432),\\n \\\"biostatistician\\\": (\\\"scientist\\\", 0.339724),\\n \\\"somewheres\\\": (\\\"somewheres\\\", 0.402736),\\n \\\"observing\\\": (\\\"observe\\\", 0.823096),\\n \\\"Leaving\\\": (\\\"leaving\\\", 1.0),\\n}\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"In the example above, the vector for “Shore” was removed and remapped to the\\nvector of “coast”, which is deemed about 73% similar. “Leaving” was remapped to\\nthe vector of “leaving”, which is identical. If you’re using the\\n\", \_jsx(\_components.a, {\n href: \"/api/cli#init-vectors\",\n children: \_jsx(InlineCode, {\n children: \"init vectors\"\n })\n }), \" command, you can set the \", \_jsx(InlineCode, {\n children: \"--prune\"\n }), \"\\noption to easily reduce the size of the vectors as you add them to a spaCy\\npipeline:\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-bash\",\n lang: \"bash\",\n children: \"$ python -m spacy init vectors en la.300d.vec.tgz /tmp/la\_vectors\_web\_md --prune 10000\\n\"\n })\n }), \_jsx(\_components.p, {\n children: \"This will create a blank spaCy pipeline with vectors for the first 10,000 words\\nin the vectors. All other words in the vectors are mapped to the closest vector\\namong those retained.\"\n })]\n }), \_jsx(\_components.h3, {\n id: \"adding-individual-vectors\",\n children: \"Adding vectors individually \"\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(InlineCode, {\n children: \"vector\"\n }), \" attribute is a \", \_jsx(\_components.strong, {\n children: \"read-only\"\n }), \" numpy or cupy array (depending on\\nwhether you’ve configured spaCy to use GPU memory), with dtype \", \_jsx(InlineCode, {\n children: \"float32\"\n }), \". The\\narray is read-only so that spaCy can avoid unnecessary copy operations where\\npossible. You can modify the vectors via the \", \_jsx(\_components.a, {\n href: \"/api/vocab\",\n children: \_jsx(InlineCode, {\n children: \"Vocab\"\n })\n }), \" or\\n\", \_jsx(\_components.a, {\n href: \"/api/vectors\",\n children: \_jsx(InlineCode, {\n children: \"Vectors\"\n })\n }), \" table. Using the\\n\", \_jsx(\_components.a, {\n href: \"/api/vocab#set\_vector\",\n children: \_jsx(InlineCode, {\n children: \"Vocab.set\_vector\"\n })\n }), \" method is often the easiest approach\\nif you have vectors in an arbitrary format, as you can read in the vectors with\\nyour own logic, and just set them with a simple loop. This method is likely to\\nbe slower than approaches that work with the whole vectors table at once, but\\nit’s a great approach for once-off conversions before you save out your \", \_jsx(InlineCode, {\n children: \"nlp\"\n }), \"\\nobject to disk.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"Adding vectors\",\n children: \"from spacy.vocab import Vocab\\n\\nvector\_data = {\\n \\\"dog\\\": numpy.random.uniform(-1, 1, (300,)),\\n \\\"cat\\\": numpy.random.uniform(-1, 1, (300,)),\\n \\\"orange\\\": numpy.random.uniform(-1, 1, (300,))\\n}\\nvocab = Vocab()\\nfor word, vector in vector\_data.items():\\n vocab.set\_vector(word, vector)\\n\"\n })\n })]\n }), \"\\n\", \_jsxs(\_components.section, {\n id: \"section-language-data\",\n children: [\_jsx(\_components.h2, {\n id: \"language-data\",\n children: \"Language Data \"\n }), \_jsx(LanguageData101, {}), \_jsx(\_components.h3, {\n id: \"language-subclass\",\n children: \"Creating a custom language subclass \"\n }), \_jsxs(\_components.p, {\n children: [\"If you want to customize multiple components of the language data or add support\\nfor a custom language or domain-specific “dialect”, you can also implement your\\nown language subclass. The subclass should define two attributes: the \", \_jsx(InlineCode, {\n children: \"lang\"\n }), \"\\n(unique language code) and the \", \_jsx(InlineCode, {\n children: \"Defaults\"\n }), \" defining the language data. For an\\noverview of the available attributes that can be overwritten, see the\\n\", \_jsx(\_components.a, {\n href: \"/api/language#defaults\",\n children: \_jsx(InlineCode, {\n children: \"Language.Defaults\"\n })\n }), \" documentation.\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n executable: \"true\",\n children: \"from spacy.lang.en import English\\n\\nclass CustomEnglishDefaults(English.Defaults):\\n stop\_words = set([\\\"custom\\\", \\\"stop\\\"])\\n\\nclass CustomEnglish(English):\\n lang = \\\"custom\_en\\\"\\n Defaults = CustomEnglishDefaults\\n\\nnlp1 = English()\\nnlp2 = CustomEnglish()\\n\\nprint(nlp1.lang, [token.is\_stop for token in nlp1(\\\"custom stop\\\")])\\nprint(nlp2.lang, [token.is\_stop for token in nlp2(\\\"custom stop\\\")])\\n\"\n })\n }), \_jsxs(\_components.p, {\n children: [\"The \", \_jsx(\_components.a, {\n href: \"/api/top-level#registry\",\n children: \_jsx(InlineCode, {\n children: \"@spacy.registry.languages\"\n })\n }), \" decorator lets you\\nregister a custom language class and assign it a string name. This means that\\nyou can call \", \_jsx(\_components.a, {\n href: \"/api/top-level#spacy.blank\",\n children: \_jsx(InlineCode, {\n children: \"spacy.blank\"\n })\n }), \" with your custom\\nlanguage name, and even train pipelines with it and refer to it in your\\n\", \_jsx(\_components.a, {\n href: \"/usage/training#config\",\n children: \"training config\"\n }), \".\"]\n }), \_jsxs(\_components.blockquote, {\n children: [\"\\n\", \_jsx(\_components.h4, {\n children: \"Config usage\"\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"After registering your custom language class using the \", \_jsx(InlineCode, {\n children: \"languages\"\n }), \" registry,\\nyou can refer to it in your \", \_jsx(\_components.a, {\n href: \"/usage/training#config\",\n children: \"training config\"\n }), \". This\\nmeans spaCy will train your pipeline using the custom subclass.\"]\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-ini\",\n lang: \"ini\",\n children: \"[nlp]\\nlang = \\\"custom\_en\\\"\\n\"\n })\n }), \"\\n\", \_jsxs(\_components.p, {\n children: [\"In order to resolve \", \_jsx(InlineCode, {\n children: \"\\\"custom\_en\\\"\"\n }), \" to your subclass, the registered function\\nneeds to be available during training. You can load a Python file containing\\nthe code using the \", \_jsx(InlineCode, {\n children: \"--code\"\n }), \" argument:\"]\n }), \"\\n\", \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-bash\",\n lang: \"bash\",\n children: \"python -m spacy train config.cfg --code code.py\\n\"\n })\n }), \"\\n\"]\n }), \_jsx(\_components.pre, {\n children: \_jsx(\_components.code, {\n className: \"language-python\",\n lang: \"python\",\n title: \"Registering a custom language\",\n highlight: \"7,12-13\",\n children: \"import spacy\\nfrom spacy.lang.en import English\\n\\nclass CustomEnglishDefaults(English.Defaults):\\n stop\_words = set([\\\"custom\\\", \\\"stop\\\"])\\n\\n@spacy.registry.languages(\\\"custom\_en\\\")\\nclass CustomEnglish(English):\\n lang = \\\"custom\_en\\\"\\n Defaults = CustomEnglishDefaults\\n\\n# This now works! 🎉\\nnlp = spacy.blank(\\\"custom\_en\\\")\\n\"\n })\n })]\n })]\n });\n}\nfunction MDXContent(props = {}) {\n const {wrapper: MDXLayout} = Object.assign({}, \_provideComponents(), props.components);\n return MDXLayout ? \_jsx(MDXLayout, Object.assign({}, props, {\n children: \_jsx(\_createMdxContent, props)\n })) : \_createMdxContent(props);\n}\nreturn {\n default: MDXContent\n};\nfunction \_missingMdxReference(id, component) {\n throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{"title":"Linguistic Features","next":"/usage/rule-based-matching","menu":[["POS Tagging","pos-tagging"],["Morphology","morphology"],["Lemmatization","lemmatization"],["Dependency Parse","dependency-parse"],["Named Entities","named-entities"],["Entity Linking","entity-linking"],["Tokenization","tokenization"],["Merging \u0026 Splitting","retokenization"],["Sentence Segmentation","sbd"],["Mappings \u0026 Exceptions","mappings-exceptions"],["Vectors \u0026 Similarity","vectors-similarity"],["Language Data","language-data"]]},"scope":{}},"sectionTitle":"Usage Documentation","theme":"blue","section":"usage","apiDetails":{"stringName":null,"baseClass":null,"trainable":null},"isIndex":false},"\_\_N\_SSG":true},"page":"/[...listPathPage]","query":{"listPathPage":["usage","linguistic-features"]},"buildId":"KWY8E8C4-tJ2EjD2\_C\_up","isFallback":false,"dynamicIds":[728,5492],"gsp":true,"scriptLoader":[]}