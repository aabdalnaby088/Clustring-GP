import json
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.output_parsers import PydanticOutputParser
from db import get_file_names, save_clusters_to_db
from models import ClusterResponse

async def cluster_files(llm):
    """Fetch file names from DB, cluster them, and store the result in MongoDB."""
    # Get file names from MongoDB
    sentences = await get_file_names()
    # Existing clusters (can be fetched from DB if needed)
    existing_clusters = []

    prompt_template = """لديك القائمة التالية من الكتب: {sentences}. لديك أيضًا المجموعات الحالية التالية: {existing_clusters}.
    قم بتوزيع الكتب على المجموعات الموجودة إذا كانت تناسبها بناءً على الموضوع، مع الحفاظ على أسماء المجموعات الحالية كما هي. إذا كان هناك كتاب لا يناسب أي مجموعة موجودة، أنشئ مجموعة جديدة له باسم عام نسبيًا (مثل "الرياضيات" أو "الاقتصاد" بدلاً من أسماء محددة جدًا). أعد النتيجة كـ JSON صالح بصيغة: {{"clusters": [{{"cluster_name": "اسم المجموعة", "points": ["عنصر1", "عنصر2"]}}, ...]}}. لا تعدل أسماء المجموعات القديمة."""

    # Use LLM to generate clustering
    program = LLMTextCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_cls=ClusterResponse),
        prompt_template_str=prompt_template,
        llm=llm,
        verbose=True,
    )

    response = program(sentences=str(sentences), existing_clusters=json.dumps(existing_clusters, ensure_ascii=False))

    # Convert response to MongoDB format
    clustered_data = [{"cluster_name": cluster.cluster_name, "points": cluster.points} for cluster in response.clusters]

    # Save clusters to MongoDB
    await save_clusters_to_db(clustered_data)

    return {'message': 'success'}
