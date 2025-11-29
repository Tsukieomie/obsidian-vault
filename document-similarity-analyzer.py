#!/usr/bin/env python3
"""
Document Similarity Analyzer
Analyzes document similarity and identifies related/duplicate content.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

class DocumentSimilarityAnalyzer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.documents = {}
        self.document_vectors = {}
        self.similarity_matrix = defaultdict(dict)
        self.document_clusters = []
        self.related_documents = defaultdict(list)

    def run_analysis(self):
        """Run document similarity analysis."""
        print("=" * 80)
        print("DOCUMENT SIMILARITY ANALYZER - CONTENT CLUSTERING")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] LOADING AND PREPROCESSING DOCUMENTS...")
        self.load_documents()

        print("\n[PHASE 2] BUILDING DOCUMENT VECTORS...")
        self.build_document_vectors()

        print("\n[PHASE 3] CALCULATING DOCUMENT SIMILARITY...")
        self.calculate_similarity()

        print("\n[PHASE 4] CLUSTERING SIMILAR DOCUMENTS...")
        self.cluster_documents()

        print("\n[PHASE 5] IDENTIFYING RELATED DOCUMENTS...")
        self.identify_related_documents()

        print("\n[PHASE 6] GENERATING SIMILARITY REPORT...")
        self.generate_similarity_report()

        print("\n" + "=" * 80)
        print("DOCUMENT SIMILARITY ANALYSIS COMPLETE")
        print("=" * 80)

    def load_documents(self):
        """Load all documents from vault."""
        print(f"\nLoading documents...")

        doc_count = 0

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                rel_path = str(file_path.relative_to(self.vault_path))
                self.documents[rel_path] = {
                    'content': content,
                    'size': len(content),
                    'words': len(content.split()),
                    'lines': len(content.split('\n'))
                }
                doc_count += 1

            except Exception as e:
                pass

        print(f"✓ Loaded {doc_count} documents")

    def build_document_vectors(self):
        """Build feature vectors for documents."""
        print(f"\nBuilding document vectors...")

        # Extract key features from each document
        for doc_path, doc_data in self.documents.items():
            content = doc_data['content']

            # Extract key terms (top n-grams)
            words = content.lower().split()
            word_freq = defaultdict(int)

            for word in words:
                clean_word = re.sub(r'[^a-z0-9]', '', word)
                if len(clean_word) > 3:  # Only significant words
                    word_freq[clean_word] += 1

            # Top 20 words form the vector
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

            self.document_vectors[doc_path] = {
                'top_words': dict(top_words),
                'vocabulary_size': len(word_freq),
                'avg_word_length': sum(len(w) for w in word_freq) / len(word_freq) if word_freq else 0
            }

        print(f"✓ Built vectors for {len(self.document_vectors)} documents")

    def calculate_similarity(self):
        """Calculate similarity between documents."""
        print(f"\nCalculating document similarity...")

        doc_paths = list(self.documents.keys())
        similarity_count = 0

        for i, doc1 in enumerate(doc_paths):
            for doc2 in doc_paths[i+1:]:
                # Jaccard similarity of top words
                words1 = set(self.document_vectors[doc1]['top_words'].keys())
                words2 = set(self.document_vectors[doc2]['top_words'].keys())

                if len(words1) > 0 and len(words2) > 0:
                    intersection = len(words1 & words2)
                    union = len(words1 | words2)
                    similarity = intersection / union

                    if similarity > 0.2:  # Threshold for relevant similarity
                        self.similarity_matrix[doc1][doc2] = similarity
                        self.similarity_matrix[doc2][doc1] = similarity
                        similarity_count += 1

        print(f"✓ Calculated {similarity_count} significant similarities")

    def cluster_documents(self):
        """Cluster similar documents together."""
        print(f"\nClustering similar documents...")

        visited = set()
        cluster_count = 0

        for doc in self.documents.keys():
            if doc not in visited:
                cluster = {doc}
                queue = [doc]

                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue

                    visited.add(current)

                    # Add similar documents
                    for similar_doc, similarity in self.similarity_matrix[current].items():
                        if similar_doc not in visited and similarity > 0.3:
                            cluster.add(similar_doc)
                            queue.append(similar_doc)

                if len(cluster) > 1:
                    self.document_clusters.append({
                        'size': len(cluster),
                        'documents': list(cluster),
                        'cluster_id': cluster_count
                    })
                    cluster_count += 1

        print(f"✓ Created {cluster_count} document clusters")

    def identify_related_documents(self):
        """Identify related documents for each document."""
        print(f"\nIdentifying related documents...")

        relation_count = 0

        for doc, similarities in self.similarity_matrix.items():
            sorted_similar = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

            for related_doc, similarity in sorted_similar[:5]:
                if similarity > 0.3:
                    self.related_documents[doc].append({
                        'document': related_doc,
                        'similarity': similarity
                    })
                    relation_count += 1

        print(f"✓ Identified {relation_count} document relationships")

    def generate_similarity_report(self):
        """Generate document similarity report."""
        report_path = self.vault_path / 'DOCUMENT_SIMILARITY_REPORT.md'

        report = []
        report.append("# DOCUMENT SIMILARITY ANALYSIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Document Clusters
        report.append("## DOCUMENT CLUSTERS\n")
        report.append(f"**Total Clusters:** {len(self.document_clusters)}\n")

        for cluster in sorted(self.document_clusters, key=lambda x: x['size'], reverse=True):
            report.append(f"\n### Cluster {cluster['cluster_id']} ({cluster['size']} documents)\n")
            for doc in cluster['documents'][:10]:
                report.append(f"- {doc}")

        # Related Documents
        report.append(f"\n## RELATED DOCUMENTS\n")
        report.append("Documents with significant content similarity:\n")

        for doc, related_list in sorted(self.related_documents.items()):
            if related_list:
                report.append(f"\n### {doc}\n")
                for rel in sorted(related_list, key=lambda x: x['similarity'], reverse=True):
                    report.append(f"- {rel['document']} (similarity: {rel['similarity']:.3f})")

        # High Similarity Pairs
        report.append(f"\n## HIGHEST SIMILARITY PAIRS\n")
        all_pairs = []
        for doc1, sims in self.similarity_matrix.items():
            for doc2, sim in sims.items():
                if doc1 < doc2:  # Avoid duplicates
                    all_pairs.append((doc1, doc2, sim))

        sorted_pairs = sorted(all_pairs, key=lambda x: x[2], reverse=True)
        for doc1, doc2, sim in sorted_pairs[:30]:
            report.append(f"- {doc1} ↔ {doc2} ({sim:.3f})")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Document similarity report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    analyzer = DocumentSimilarityAnalyzer(vault_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
