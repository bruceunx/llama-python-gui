from pathlib import Path

base_path = Path(__file__).resolve().parent

code_style: str = """
<style>
pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.codehilite .hll { background-color: #49483e }
.codehilite { background: #272822; color: #f8f8f2; }
.codehilite .c { color: #959077 } /* Comment */
.codehilite .err { color: #ed007e; background-color: #1e0010 } /* Error */
.codehilite .esc { color: #f8f8f2 } /* Escape */
.codehilite .g { color: #f8f8f2 } /* Generic */
.codehilite .k { color: #66d9ef } /* Keyword */
.codehilite .l { color: #ae81ff } /* Literal */
.codehilite .n { color: #f8f8f2 } /* Name */
.codehilite .o { color: #ff4689 } /* Operator */
.codehilite .x { color: #f8f8f2 } /* Other */
.codehilite .p { color: #f8f8f2 } /* Punctuation */
.codehilite .ch { color: #959077 } /* Comment.Hashbang */
.codehilite .cm { color: #959077 } /* Comment.Multiline */
.codehilite .cp { color: #959077 } /* Comment.Preproc */
.codehilite .cpf { color: #959077 } /* Comment.PreprocFile */
.codehilite .c1 { color: #959077 } /* Comment.Single */
.codehilite .cs { color: #959077 } /* Comment.Special */
.codehilite .gd { color: #ff4689 } /* Generic.Deleted */
.codehilite .ge { color: #f8f8f2; font-style: italic } /* Generic.Emph */
.codehilite .ges { color: #f8f8f2; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.codehilite .gr { color: #f8f8f2 } /* Generic.Error */
.codehilite .gh { color: #f8f8f2 } /* Generic.Heading */
.codehilite .gi { color: #a6e22e } /* Generic.Inserted */
.codehilite .go { color: #66d9ef } /* Generic.Output */
.codehilite .gp { color: #ff4689; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { color: #f8f8f2; font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #959077 } /* Generic.Subheading */
.codehilite .gt { color: #f8f8f2 } /* Generic.Traceback */
.codehilite .kc { color: #66d9ef } /* Keyword.Constant */
.codehilite .kd { color: #66d9ef } /* Keyword.Declaration */
.codehilite .kn { color: #ff4689 } /* Keyword.Namespace */
.codehilite .kp { color: #66d9ef } /* Keyword.Pseudo */
.codehilite .kr { color: #66d9ef } /* Keyword.Reserved */
.codehilite .kt { color: #66d9ef } /* Keyword.Type */
.codehilite .ld { color: #e6db74 } /* Literal.Date */
.codehilite .m { color: #ae81ff } /* Literal.Number */
.codehilite .s { color: #e6db74 } /* Literal.String */
.codehilite .na { color: #a6e22e } /* Name.Attribute */
.codehilite .nb { color: #f8f8f2 } /* Name.Builtin */
.codehilite .nc { color: #a6e22e } /* Name.Class */
.codehilite .no { color: #66d9ef } /* Name.Constant */
.codehilite .nd { color: #a6e22e } /* Name.Decorator */
.codehilite .ni { color: #f8f8f2 } /* Name.Entity */
.codehilite .ne { color: #a6e22e } /* Name.Exception */
.codehilite .nf { color: #a6e22e } /* Name.Function */
.codehilite .nl { color: #f8f8f2 } /* Name.Label */
.codehilite .nn { color: #f8f8f2 } /* Name.Namespace */
.codehilite .nx { color: #a6e22e } /* Name.Other */
.codehilite .py { color: #f8f8f2 } /* Name.Property */
.codehilite .nt { color: #ff4689 } /* Name.Tag */
.codehilite .nv { color: #f8f8f2 } /* Name.Variable */
.codehilite .ow { color: #ff4689 } /* Operator.Word */
.codehilite .pm { color: #f8f8f2 } /* Punctuation.Marker */
.codehilite .w { color: #f8f8f2 } /* Text.Whitespace */
.codehilite .mb { color: #ae81ff } /* Literal.Number.Bin */
.codehilite .mf { color: #ae81ff } /* Literal.Number.Float */
.codehilite .mh { color: #ae81ff } /* Literal.Number.Hex */
.codehilite .mi { color: #ae81ff } /* Literal.Number.Integer */
.codehilite .mo { color: #ae81ff } /* Literal.Number.Oct */
.codehilite .sa { color: #e6db74 } /* Literal.String.Affix */
.codehilite .sb { color: #e6db74 } /* Literal.String.Backtick */
.codehilite .sc { color: #e6db74 } /* Literal.String.Char */
.codehilite .dl { color: #e6db74 } /* Literal.String.Delimiter */
.codehilite .sd { color: #e6db74 } /* Literal.String.Doc */
.codehilite .s2 { color: #e6db74 } /* Literal.String.Double */
.codehilite .se { color: #ae81ff } /* Literal.String.Escape */
.codehilite .sh { color: #e6db74 } /* Literal.String.Heredoc */
.codehilite .si { color: #e6db74 } /* Literal.String.Interpol */
.codehilite .sx { color: #e6db74 } /* Literal.String.Other */
.codehilite .sr { color: #e6db74 } /* Literal.String.Regex */
.codehilite .s1 { color: #e6db74 } /* Literal.String.Single */
.codehilite .ss { color: #e6db74 } /* Literal.String.Symbol */
.codehilite .bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #a6e22e } /* Name.Function.Magic */
.codehilite .vc { color: #f8f8f2 } /* Name.Variable.Class */
.codehilite .vg { color: #f8f8f2 } /* Name.Variable.Global */
.codehilite .vi { color: #f8f8f2 } /* Name.Variable.Instance */
.codehilite .vm { color: #f8f8f2 } /* Name.Variable.Magic */
.codehilite .il { color: #ae81ff } /* Literal.Number.Integer.Long */
</style>
"""

MODEL_PATH = {
    "normal": "../llm/models/openhermes-2.5-mistral-7b.Q5_K_M.gguf",
    "small": "../llm/models/openhermes-2.5-mistral-7b.Q5_K_M.gguf"
}
