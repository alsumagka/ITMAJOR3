from fastapi import FastAPI, HTTPException
import sqlite3
from typing import List
import schema

app = FastAPI()

def db():
    con = sqlite3.connect("final.db")
    con.row_factory=sqlite3.Row
    return con


@app.post("/user")
async def user(reg: schema.users):
    con = db()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password, firstname, lastname) VALUES (?, ? ,? ,?)", (reg.username, reg.password, reg.firstname, reg.lastname))
        con.commit()
        msg = "Registered Successfully"
    except sqlite3.Error as error:
        con.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
    finally:
        con.close()

    return msg

@app.put("/user/{id}")
async def change(id, reg: schema.users):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    dats = cur.fetchone()

    if dats is None:
        raise HTTPException(status_code=404, detail="No user found")
    else:
        try:
            cur.execute("UPDATE users SET username=?, password=?, firstname=?, password=? WHERE id = ? ", (reg.username, reg.password, reg.firstname, reg.lastname, id))
            con.commit()
            msg = "Updated Successfully"
        except sqlite3.Error as error:
            con.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: f{error}")
        finally:
            con.close()
    
    return msg

@app.delete("/user{id}")
async def deleteuser(id):
    con = db()
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (id,))
        con.commit()
        msg = "Successfully Deleted"
    except sqlite3.Error as error:
        con.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
    finally:
        con.close()
    
    return msg
#----------------------------------------------------------------SERIES----------------------------------------------------------------------------

@app.get("/series", response_model=List[schema.RemindMe])
async def series():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM media")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="Empty")

    return [dict(row) for row in dats]

@app.post("/series")
async def addSeries(addmed: schema.RemindMe):
    con = db()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO media (type, title, description, day) VALUES (?, ?, ?, ?)", (addmed.type, addmed.title, addmed.description, addmed.day))
        con.commit()
        message = "Added Successfully"
    
    except sqlite3.Error as error:
        con.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
    
    finally:
        con.close

    return message

@app.put("/series/{id}")
async def updateSeries(id, updet: schema.RemindMe):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM media WHERE id = ?", (id,))
    dats = cur.fetchone()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    else:
        try:
            cur.execute("UPDATE media SET type = ?, title = ?, description = ?, day = ? WHERE id = ?",(updet.type, updet.title, updet.description, updet.day, id))
            con.commit()
            message = "Updated Successfully"

        except sqlite3.Error as error:
            con.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {error}")
        
        finally:
            con.close()
    
    return message

@app.delete("/series/{id}")
async def deleteSeries(id):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM media WHERE id = ?", (id,))
    dats = cur.fetchone()

    if not dats:
        raise HTTPException(status_code=404, detail="No result")
    else:
        try:
            cur.execute("DELETE FROM media WHERE id = ?", (id,))
            con.commit()
            message = "Deleted Successfully"

        except sqlite3.Error as error:
            con.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {error}")
        
        finally:
            con.close()

    return message

@app.get("/series/anime", response_model=List[schema.RemindMe])
async def anime():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM media WHERE type = anime")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [i for i in dats]

@app.get("/series/kdrama/", response_model=List[schema.RemindMe])
async def kdrama():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM media WHERE type = kdrama")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [i for i in dats]

@app.get("/series/", response_model=List[schema.RemindMe])
async def seriesHistory():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM serieshist")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [dict(i) for i in dats]
#--------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------MOVIES--------------------------------------------------------------------------
@app.get("/movies", response_model=List[schema.Movies])
async def viewMovies():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM movies")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [dict(i) for i in dats]

@app.post("/movies")
async def addMovies(add: schema.Movies):
    con = db()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO movieS (title, description, day) VALUES (?, ?, ?)", (add.title, add.description, add.day))
        con.commit()
        message = "Added Successfully"

    except sqlite3.Error as error:
        con.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
    
    finally:
        con.close()

    return message

@app.put("/movies/{id}")
async def updateMovies(id, update: schema.Movies):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM movies WHERE id = ?", (id,))
    dats = cur.fetchone()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    else:
        try:
            cur.execute("UPDATE movies SET title =?, description = ?, day = ? WHERE id = ?", (update.title, update.description, update.day, id))
            con.commit()
            message = "Updated Successfully"
        
        except sqlite3.Error as error:
            con.close()
            raise HTTPException(status_code=500, detail=f"Database error: {error}")
        
        finally:
            con.close()

    return message

@app.delete("/movies/{id}")
async def deleteMovies(id):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM movies WHERE id = ?", (id,))
    dats = cur.fetchone()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    else:
        try:
            cur.execute("DELETE FROM movies WHERE id = ?", (id,))
            con.commit()
            message = "Deleted Successfully"
        
        except sqlite3.Error as error:
            con.close()
            raise HTTPException(status_code=500, detail=f"Database Error: {error}")
        
        finally:
            con.close()
    
    return message

@app.get("/movies/", response_model=List[schema.Movies])
async def movieHistory():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM moviehist")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [dict(i) for i in dats]

#--------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------MANGA--------------------------------------------------------------------------

@app.get("/manga", response_model=List[schema.ResponseManga])
async def viewManga():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM manga")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [dict(i) for i in dats]

@app.post("/manga")
async def addManga(add: schema.addManga):
    con = db()
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO manga (type, title, description, day) VALUES (?, ?, ?, ?)", (add.type, add.title, add.description, add.day))
        con.commit()
        message = "Added Successfully"

    except sqlite3.Error as error:
        con.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
    
    finally:
        con.close()

    return message

@app.put("/manga/{id}")
async def updateManga(id, update: schema.updateManga):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM manga WHERE id = ?", (id,))
    dats = cur.fetchone()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    else:
        try:
            cur.execute("UPDATE manga SET type = ?, title =?, description = ?, day = ? WHERE id = ?", (update.type, update.title, update.description, update.day, id))
            con.commit()
            message = "Updated Successfully"
        
        except sqlite3.Error as error:
            con.close()
            raise HTTPException(status_code=500, detail=f"Database error: {error}")
        
        finally:
            con.close()

    return message

@app.delete("/manga/{id}")
async def deleteManga(id):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM manga WHERE id = ?", (id,))
    dats = cur.fetchone()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    else:
        try:
            cur.execute("DELETE FROM manga WHERE id = ?", (id,))
            con.commit()
            message = "Deleted Successfully"
        
        except sqlite3.Error as error:
            con.close()
            raise HTTPException(status_code=500, detail=f"Database Error: {error}")
        
        finally:
            con.close()
    
    return message

@app.get("/manga/", response_model=List[schema.ResponseManga])
async def mangaHistory():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM mangahist")
    dats = cur.fetchall()

    if not dats:
        con.close()
        raise HTTPException(status_code=404, detail="No result")
    
    return [dict(i) for i in dats]

#--------------------------------------------------------------------------------------------------------------------------------------------------