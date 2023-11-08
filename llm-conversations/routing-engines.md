> % llm chat -m 4t 

Chatting with gpt-4-1106-preview

> I am interested in learning about the options in open-source routing engines, ie to find a route through a map. This is primarily so I can learn how they work, so one that has good ease-of-use, but is also legible in terms of inspecting how it came to a decision would be great. I am most familiar with Python, but not limited to it. In future I would enjoy being able to introduce new algorithms such as for real-time public transit route planning that includes legs on a bike.

Open-source routing engines are powerful tools used for pathfinding and navigation on geographic data. Many are built to work with OpenStreetMap data, and they offer various features, including vehicle-specific routing, real-time updates, and multimodal transportation options. Below are some of the popular open-source routing engines:

1. **GraphHopper**:
   - Written in Java.
   - Offers routing for cars, bikes, walking, and public transport.
   - Has both a fast and customizable routing engine.
   - Provides APIs for routing, map matching, and matrix routing.
   - You can easily set up a server and integrate with other Java projects.
   - Website: https://www.graphhopper.com/

2. **Valhalla**:
   - Written in C++.
   - Provides APIs for various types of routing (including time/distance matrix computation, map matching, and multimodal routing).
   - Used by the Mapzen Turn-by-Turn navigation product.
   - Active development community, and it is easy to use for developers familiar with C++ or willing to set up service via Docker.
   - Website: https://github.com/valhalla/valhalla

3. **OSRM (Open Source Routing Machine)**:
   - Written in C++.
   - Ideal for high-performance routing and designed primarily for car routing, but can also be used for bikes and pedestrians.
   - It pre-processes the map data to allow for extremely fast routing query responses.
   - Well-documented and has a robust HTTP API.
   - Website: http://project-osrm.org/

4. **OpenTripPlanner (OTP)**:
   - Written in Java.
   - Focused on multimodal trip planning, including public transportation.
   - Supports integration with real-time transit data.
   - It allows for custom routing profiles and considerable extensibility.
   - Website: http://www.opentripplanner.org/

5. **PgRouting**:
   - Extension of PostgreSQL/PostGIS.
   - Offers routing functionality to the database.
   - It uses SQL for route querying, so it’s a good choice if you’re familiar with databases.
   - Supports various routing algorithms, including A*, Dijkstra, and more.
   - Website: https://pgrouting.org/

Since you mentioned Python, you can interact with most of these routing engines via their HTTP APIs using Python libraries such as `requests`. Additionally, OSRM and GraphHopper, for instance, have Python clients that can facilitate the interaction between your Python code and the routing engine.

Whichever routing engine you choose will depend on your specific needs and preferences. If you aim to work with public transit route planning and are interested in integrating bike routes, OpenTripPlanner might be the most suitable given its focus on multimodal transportation.

Keep in mind that if you want to introduce new algorithms or modify existing ones, you might need to delve into the engine's core code (which could be in Java, C++, etc.) and have a good understanding of both geographic information systems (GIS) and routing algorithms.

For understanding how these engines work, ensure you look for projects with good documentation and an active community. This would help you get started and also provide insight into algorithmic decisions and trade-offs. Since these are open-source projects, you can inspect the code, follow the issue tracker discussions, and engage with the community through mailing lists or chat channels to better understand how the routing decisions are made.

> What is the relative popularity of each of those? And I know of at least one other one; bRouter.

As of my knowledge cutoff date in early 2023, each routing engine mentioned has a certain level of popularity and use cases that it's particularly suited to. Popularity can vary based on the application (such as car navigation vs. multimodal transport planning), geographic location, community size, and ease of use. However, it's not easy to quantify their popularity with exact metrics since usage may span across closed and open-source projects, non-commercial and commercial applications, and community or proprietary deployments. Here's a brief overview:

1. **OSRM (Open Source Routing Machine)**: OSRM is very popular for car and bike routing services due to its high performance for point-to-point routing. It's favored for applications requiring high-volume and rapid responses.

2. **GraphHopper**: This is another popular engine and it's known for its straightforward integration with Java applications. It is versatile, with routing for cars, bikes, and walking, and it also has a community that contributes to public transport solutions.

3. **Valhalla**: Developed by Mapzen and taken over by the Linux Foundation's Urban Computing Foundation, Valhalla has been gaining in popularity, especially with applications that benefit from its multimodal routing capabilities and rich narrative instructions.

4. **OpenTripPlanner (OTP)**: OTP is a leading solution for multimodal and public transit routing, and it's used by transportation agencies and planners around the world. It offers a unique set of features for those who need to incorporate transit systems into their routing solutions.

5. **PgRouting**: This engine is popular in the database community, particularly among those who work heavily with PostGIS and PostgreSQL. It's a staple for users who need routing capabilities integrated with SQL and spatial databases.

Regarding **bRouter** (which stands for "bike router"):
- **bRouter**: It's a lesser-known but specialized routing engine aimed at bicycle routing, with a focus on finding the most bike-friendly routes. It is available as both a web service and a smartphone app and allows users to customize their routes in detail. The project emphasizes customizable profiles, allowing for fine-grained control over routing preferences.

bRouter could be considered a niche tool compared to some of the other more general-purpose routing engines, but it's highly regarded within the cycling community for its detailed attention to the needs of cyclists.

To gauge the relative popularity, you might look at various indicators such as the number of GitHub stars, frequency of commits, number of contributors, and the activity on community forums and mailing lists. Keep in mind that popularity doesn't necessarily equate to suitability for a given task; it's important to choose a routing engine based on the specific requirements of your project and the kind of support and feature set you're looking for.

