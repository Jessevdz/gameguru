from typing import List
import chromadb
from embed import Embedder, GTEEmbedder


class VectorDB:
    def __init__(
        self,
        db_loc: str = "db.chroma",
        embedder: Embedder = GTEEmbedder(),
    ):
        self.client = chromadb.PersistentClient(path=db_loc)
        self.embedder = embedder
        self.games = [c.name for c in self.client.list_collections()]

    def add(self, game: str, documents: List[str]):
        """
        Embed documents and add them to the vector store, for a specific game.
        """
        assert game not in self.games, "Game already exists in database."
        collection = self.client.create_collection(name=game)
        ids: List[str] = [f"{game}_{str(i)}" for i in range(len(documents))]
        embeddings: List[List[float]] = self.embedder.embed(documents).tolist()
        collection.add(ids=ids, embeddings=embeddings, documents=documents)
        self.games.append(game)

    def get_related_documents(self, game: str, query: str, n_results: int = 3):
        """
        Return most similar documents for a game, relative to a specific query.
        """
        assert game in self.games, "Game does not exist in database."
        collection = self.client.get_collection(name=game)
        query_embedding = self.embedder.embed([query]).tolist()
        results = collection.query(
            query_embeddings=query_embedding, n_results=n_results
        )
        return results["documents"][0]

    def list_games(self) -> str:
        """
        Return all games that have rules in the database as a comma separated string.
        """
        return ",".join([c.name for c in self.client.list_collections()])
