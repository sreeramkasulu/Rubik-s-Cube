import uvicorn
from fastapi import FastAPI
from fastapi.params import Query
from fastapi.middleware.cors import CORSMiddleware
from rubik.cubes import Cube
from rubik.solvers import KociembaSolver


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")




@app.get("/api/solve")
async def solve(cube_str: str = Query(..., alias="cube", min_length=54, max_length=54)):  
    
    cube: Cube
    solver: KociembaSolver
    try:
        cube = Cube(cube_str)
    except ValueError as e:
        print(str(e))
        return {"error": str(e)}

    try:
        solver = KociembaSolver(cube)
        solver.solve()
    except KeyError as e:  
        return {"error": "Piece for a color is missing."}
    except Exception as e:
        return {"error": str(e)}

    return {
        "cube": str(cube),
        "moves": solver.moves,
        "timeToSolve": solver.time_to_solve,
    }


if __name__ == "__main__":
    uvicorn.run("index:app", host="localhost", port=8000, reload=True)
